from rest_framework.viewsets import (
    ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
)
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin,
    CreateModelMixin, UpdateModelMixin,
)
from users import serializers as UsersSerializers
from users import models as UsersModels
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from core.helper import (
    update_status_value
)


# Follow APIs
class FollowView(UpdateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet, CreateModelMixin,):
    """
    A view for follow and unfollow users by themselves (create, update, get)
    """
    serializer_class = UsersSerializers.FollowSerializer
    queryset = UsersModels.Follow.objects.all()

    def update(self, request: Request, *args, **kwargs):
        return update_status_value(
            request=request, self=self,
            status_class=UsersModels.Follow.Status,
            seriaizer=UsersSerializers.FollowSerializer
        )

    def create(self, request: Request, *args, **kwargs):
        data = request.data

        if data['status'] != UsersModels.Follow.Status.FOLLOEWED:
            return Response(
                data={
                    "error": 'Wrong data.',
                    "details": f"The value of status have to be {UsersModels.Follow.Status.FOLLOEWED}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        flr_user = data['follower_user']
        fld_user = data['followed_user']

        if fld_user == flr_user:
            return Response(
                {"detail": f"One user cannot follow himself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        found = UsersModels.Follow.objects.filter(Q(
            followed_user=fld_user, flr_user=flr_user
        ))

        if found:
            return Response(
                {"details": f"This {data['follower_user']} user has already follow this {data['followed_user']} user", },
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            super().create(request, *args, **kwargs)


# Login APIs
class LoginsView(ReadOnlyModelViewSet):
    """
    A view for set log about login tries by users
    """
    serializer_class = UsersSerializers.LoginsSerializers
    queryset = UsersModels.Logins.objects.all()
