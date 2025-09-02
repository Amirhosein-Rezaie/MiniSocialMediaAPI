from rest_framework.viewsets import (
    ModelViewSet, GenericViewSet
)
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin, CreateModelMixin
)
from core import serializers as CoreSerializers
from core import models as CoreModels
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status


# Users APIs
class UserView(ModelViewSet):
    """
    A view for delete, create, get and update users
    """
    serializer_class = CoreSerializers.UsersSerializer
    queryset = CoreModels.Users.objects.all()

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.status = CoreModels.Users.Status.IS_DELETED
        obj.save()
        return Response(
            data=CoreSerializers.UsersSerializer(obj).data,
            status=status.HTTP_200_OK
        )


# Texts APIs
class TextsView(
    GenericViewSet, RetrieveModelMixin, ListModelMixin, CreateModelMixin
):
    """
    A view for get and create texts
    """
    serializer_class = CoreSerializers.TextsSerializer
    queryset = CoreModels.Texts.objects.all()


# Videos APIs
class VideosView(
    GenericViewSet, RetrieveModelMixin, ListModelMixin, CreateModelMixin
):
    """
    A view for get and create video
    """
    serializer_class = CoreSerializers.VideosSerializer
    queryset = CoreModels.Videos.objects.all()


# Videos APIs
class ImagesView(
    GenericViewSet, RetrieveModelMixin, ListModelMixin, CreateModelMixin
):
    """
    A view for get and create image
    """
    serializer_class = CoreSerializers.ImagesSerializer
    queryset = CoreModels.Images.objects.all()


# Posts APIs
class PostsView(ModelViewSet):
    """
    A view for delete, create, get and update posts
    """
    serializer_class = CoreSerializers.PostsSerializer
    queryset = CoreModels.Posts.objects.all()
