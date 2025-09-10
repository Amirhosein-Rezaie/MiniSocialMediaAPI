from rest_framework.viewsets import (
    ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
)
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin,
    CreateModelMixin, DestroyModelMixin,
)
from users import serializers as UsersSerializers
from users import models as UsersModels
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from core.helper import (
    IS_SELF_OR_READONLY_PERMISSIONS, dynamic_search, set_queryset, ONLY_USER_PERMISSIONS
)
from drf_spectacular.utils import (
    extend_schema, OpenApiParameter
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)
from core.permissions import (
    IsActive, IsAnonymous, IsSelfOrReadOnly, IsUser
)
from core.models import Users
from core.serializers import UsersSerializer
from rest_framework.exceptions import ValidationError


# Follow APIs
class FollowView(DestroyModelMixin, ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = UsersSerializers.FollowSerializer
    queryset = UsersModels.Follow.objects.all()
    permission_classes = IS_SELF_OR_READONLY_PERMISSIONS

    def get_queryset(self):
        request = self.request

        if request.user.role == Users.Roles.USER:
            return UsersModels.Follow.objects.filter(
                Q(follower_user=request.user.pk) |
                Q(followed_user=request.user.pk)
            )

        return super().get_queryset()

    def get_permissions(self):
        request = self.request

        if request.method in ['POST', 'DELETE']:
            return [IsUser()]

        return super().get_permissions()

    @extend_schema(
        description="""
        Get request of users returns all of the Follow.
        for search in them and all of fields (foreign, normal) can use queryparmas.
        """,
        parameters=[
            OpenApiParameter(
                name='follower_user-id', description="An example as foreign field in search (?follower_user-id=1)", required=False,
            ),
            OpenApiParameter(
                name='page', type=int, description="Page number to return.", required=False,
            ),
            OpenApiParameter(
                name='limit', type=int, description="Number of items per page.", required=False,
            ),
        ]
    )
    def list(self, request: Request, *args, **kwargs):
        if request.query_params:
            return dynamic_search(self, request, UsersModels.Follow)
        return super().list(request, *args, **kwargs)

    def create(self, request: Request, *args, **kwargs):
        # define allowed statuses and roles
        active_status = Users.Status.ACTIVE
        out_users = [
            Users.Roles.ADMIN.value
        ] + [s.value for s in Users.Status if s != active_status]

        data = request.data

        # get follower and followed users, raise if not found
        follower_user = None
        followed_user = None
        try:
            follower_user = Users.objects.get(id=request.user.pk)
            followed_user = Users.objects.get(id=data['followed_user'])
        except Users.DoesNotExist:
            raise ValidationError(
                detail="Users does not exist.", code=400,
            )

        # prevent self-follow
        if followed_user == follower_user:
            raise ValidationError(
                detail="Follower and followed user cannot be the same.", code=400
            )

        # prevent admin or inactive/deleted users from following
        if any(u.status in out_users or u.role in out_users for u in [followed_user, follower_user]):
            raise ValidationError(
                detail=f"Follower and followed user should not be in {out_users}.", code=400
            )

        # prevent duplicate follow
        found = UsersModels.Follow.objects.filter(Q(
            followed_user=followed_user, follower_user=follower_user
        )).exists()

        if found:
            return Response(
                {"details": "These users are already following each other."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # create follow relationship
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(follower_user=self.request.user)
        return super().perform_create(serializer)


# Login APIs
class LoginsView(ReadOnlyModelViewSet):
    serializer_class = UsersSerializers.LoginsSerializers
    queryset = UsersModels.Logins.objects.all()

    def get_queryset(self):
        return set_queryset(self, Users.Roles.USER, 'user', self.request.user.pk, UsersModels.Logins)

    @extend_schema(
        description="""
        Get request of users returns all of the Logins.
        for search in them and all of fields (foreign, normal) can use queryparmas.
        """,
        parameters=[
            OpenApiParameter(
                name='user-id', description="An example as foreign field in search (?user-id=1)", required=False,
            ),
            OpenApiParameter(
                name='username', description="An example as foreign field in search (?username=abc)", required=False,
            ),
            OpenApiParameter(
                name='page', type=int, description="Page number to return.", required=False,
            ),
            OpenApiParameter(
                name='limit', type=int, description="Number of items per page.", required=False,
            ),
        ]
    )
    def list(self, request: Request, *args, **kwargs):
        if request.query_params:
            return dynamic_search(self, request, UsersModels.Logins)
        return super().list(request, *args, **kwargs)


# generate token view
class TokenObtianView(TokenObtainPairView):
    permission_classes = [IsAnonymous]
    serializer_class = UsersSerializers.TokenSerializer


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='limit', type=int, required=False, description="set page_size of pagination."
        ),
        OpenApiParameter(
            name='page', type=int, description="Page number to return.", required=False,
        ),
        OpenApiParameter(
            name='limit', type=int, description="Number of items per page.", required=False,
        ),
    ],
    responses=UsersSerializer(many=True)
)
class MyFollowers(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    API endpoint that returns a paginated list of the current user's followers.

    - Requires the user to be authenticated with `IsUser` permission.
    - Fetches all users who follow the current user.
    - Only includes followers whose account status is ACTIVE.
    - Supports dynamic pagination based on request parameters.
    """
    permission_classes = ONLY_USER_PERMISSIONS
    serializer_class = UsersSerializer

    def get_queryset(self):
        user = self.request.user

        # Get the list of user IDs who follow the current user
        followers_id_list = UsersModels.Follow.objects.filter(
            Q(followed_user=user)
        ).values_list('follower_user', flat=True)

        # Filter active users from the followers list
        users = Users.objects.filter(
            Q(id__in=followers_id_list) & Q(status=Users.Status.ACTIVE)
        )
        return users


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='limit', type=int, required=False, description="set page_size of pagination."
        ),
        OpenApiParameter(
            name='page', type=int, description="Page number to return.", required=False,
        ),
    ],
    responses=UsersSerializer(many=True)
)
class MyFollowings(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    API endpoint that returns a paginated list of the current user's followings.

    - Requires the user to be authenticated with `IsUser` permission.
    - Fetches all users that the current user is following.
    - Only includes followings whose account status is ACTIVE.
    - Supports dynamic pagination based on request parameters.
    """
    permission_classes = ONLY_USER_PERMISSIONS
    serializer_class = UsersSerializer

    def get_queryset(self):
        user = self.request.user

        # Get the list of user IDs that the current user is following
        followings_id_list = UsersModels.Follow.objects.filter(
            Q(follower_user=user)
        ).values_list('followed_user', flat=True)

        # Filter active users from the followings list
        users = Users.objects.filter(
            Q(id__in=followings_id_list) & Q(status=Users.Status.ACTIVE)
        )
        return users
