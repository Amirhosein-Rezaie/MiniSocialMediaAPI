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


# Follow APIs
class FollowView(DestroyModelMixin, ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    """
    A view for follow and unfollow users by themselves (create, update, get)
    """
    serializer_class = UsersSerializers.FollowSerializer
    queryset = UsersModels.Follow.objects.all()

    def list(self, request: Request, *args, **kwargs):
        """
        Return all of field.
        search with query params.
        """
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
    """
    A view for set log about login tries by users
    """
    serializer_class = UsersSerializers.LoginsSerializers
    queryset = UsersModels.Logins.objects.all()

    def list(self, request: Request, *args, **kwargs):
        """
        Return all of field.
        search with query params.
        """
        if request.query_params:
            return dynamic_search(self, request, UsersModels.Logins)
        return super().list(request, *args, **kwargs)
