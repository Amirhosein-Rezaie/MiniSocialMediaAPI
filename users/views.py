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
from core.helper import (dynamic_search)
from drf_spectacular.utils import (
    extend_schema, OpenApiParameter
)


# Follow APIs
class FollowView(DestroyModelMixin, ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = UsersSerializers.FollowSerializer
    queryset = UsersModels.Follow.objects.all()

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
