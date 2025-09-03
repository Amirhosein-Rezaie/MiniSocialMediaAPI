from rest_framework.viewsets import (
    ModelViewSet, GenericViewSet,
)
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
)
from posts import serializers as PostsSerializers
from posts import models as PostsModels
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from core.helper import (
    update_status_value
)
from rest_framework.request import Request


# Albums APIs
class AlbumsView(ModelViewSet):
    """
    A view for delete, create, get and update albums
    """
    serializer_class = PostsSerializers.AlbumsSerializer
    queryset = PostsModels.Albums.objects.all()

    def update(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        update_field_value = request.data.get('title')

        if update_field_value is None:
            return Response({"detail": "title is required"}, status=status.HTTP_400_BAD_REQUEST,)

        instance.title = update_field_value
        instance.save(update_fields=['title'])
        return Response(PostsSerializers.AlbumsSerializer(instance).data, status=status.HTTP_200_OK)


# SavePosts APIs
class SavePostsView(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """
    A view for create, get and saveposts
    """
    serializer_class = PostsSerializers.SavePostSerializer
    queryset = PostsModels.SavePosts.objects.all()


# LikePost APIs
class LikePostView(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    GenericViewSet
):
    """
    A view for like and dislike a post (get, create and update)
    """
    serializer_class = PostsSerializers.LikePostSerializer
    queryset = PostsModels.LikePost.objects.all()

    def create(self, request, *args, **kwargs):
        return update_status_value(
            request=request, self=self, status_class=PostsModels.LikePost.Status,
            seriaizer=PostsSerializers.LikePostSerializer
        )


# Comments APIs
class CommentsView(ModelViewSet):
    """
    A view for comment about a posts (create, get, update and delete)
    """
    serializer_class = PostsSerializers.CommentsSerializer
    queryset = PostsModels.Comments.objects.all()

    def update(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        update_field_value = request.data.get('comment')

        if update_field_value is None:
            return Response({"detail": "comment is required"}, status=status.HTTP_400_BAD_REQUEST,)

        instance.comment = update_field_value
        instance.save(update_fields=['comment'])
        return Response(PostsSerializers.CommentsSerializer(instance).data, status=status.HTTP_200_OK)


class ViewPostView(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    """
    A view for take view of a posts (create and get)
    """
    serializer_class = PostsSerializers.ViewPostSerializer
    queryset = PostsModels.ViewPost.objects.all()
