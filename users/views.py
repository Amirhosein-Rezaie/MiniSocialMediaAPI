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
from core.helper import (dynamic_search, set_queryset, limit_paginate)
from drf_spectacular.utils import (
    extend_schema, OpenApiParameter
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)
from core.permissions import (
    IsAnonymous, IsUser
)
from core.models import Users
from core.serializers import UsersSerializer
from rest_framework.views import APIView
from core.paginations import DynamicPagination


# Follow APIs
class FollowView(DestroyModelMixin, ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = UsersSerializers.FollowSerializer
    queryset = UsersModels.Follow.objects.all()

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
        ]
    )
    def list(self, request: Request, *args, **kwargs):
        if request.query_params:
            return dynamic_search(self, request, UsersModels.Follow)
        return super().list(request, *args, **kwargs)

    def create(self, request: Request, *args, **kwargs):
        data = request.data

        flr_user = data['follower_user']
        fld_user = data['followed_user']

        found = UsersModels.Follow.objects.filter(Q(
            followed_user=fld_user, follower_user=flr_user
        ))

        if found:
            return Response(
                {"details": f"This user({data['follower_user']}) has already follow this user({data['followed_user']})", },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().create(request, *args, **kwargs)


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
        ]
    )
    def list(self, request: Request, *args, **kwargs):
        if request.query_params:
            return dynamic_search(self, request, UsersModels.Logins)
        return super().list(request, *args, **kwargs)


# generate token view
class TokenObtianView(TokenObtainPairView):
    permission_classes = [IsAnonymous]


paginator = DynamicPagination()


class MyFollowers(APIView):
    """
    API endpoint that returns a paginated list of the current user's followers.

    - Requires the user to be authenticated with `IsUser` permission.
    - Fetches all users who follow the current user.
    - Only includes followers whose account status is ACTIVE.
    - Supports dynamic pagination based on request parameters.
    """
    permission_classes = [IsUser]

    def get(self, request: Request):
        user = request.user

        # Get the list of user IDs who follow the current user
        followers_id_list = UsersModels.Follow.objects.filter(
            Q(followed_user=user)
        ).values_list('follower_user', flat=True)

        # Filter active users from the followers list
        users = Users.objects.filter(
            Q(id__in=followers_id_list) & Q(status=Users.Status.ACTIVE)
        )

        # Apply dynamic pagination based on request parameters
        paginator.page_size = limit_paginate(request, DynamicPagination)
        paginated_data = paginator.paginate_queryset(users, request)

        # Serialize the paginated users data
        serialized_data = UsersSerializer(paginated_data, many=True)

        # Return paginated response with serialized data
        return paginator.get_paginated_response(serialized_data.data)
