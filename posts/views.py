from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    GenericAPIView
)
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin, CreateModelMixin
)
from posts import serializers as PostsSerializers
from posts import models as PostsModels
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status


# Albums APIs
class AlbumsView(ModelViewSet):
    """
    A view for delete, create, get and update albums
    """
    serializer_class = PostsSerializers.AlbumsSerializer
    queryset = PostsModels.Albums.objects.all()


# SavePosts APIs
class SavePostsView(GenericAPIView, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """
    A view for create, get and update saveposts
    """
    serializer_class = PostsSerializers.SavePostSerializer
    queryset = PostsModels.SavePosts.objects.all()


# LikePost APIs
class LikePostView(GenericAPIView, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """
    A view for like and dislike a post (get, create and update)
    """
    serializer_class = PostsSerializers.LikePostSerializer
    queryset = PostsModels.LikePost.objects.all()


# Comments APIs
class CommentsView(ModelViewSet):
    """
    A view for comment about a posts (create, get, update and delete)
    """
    serializer_class = PostsSerializers.CommentsSerializer
    queryset = PostsModels.Comments.objects.all()


class ViewPostView(ModelViewSet):
    """
    A view for take view of a posts (create, update, get and delete)
    """
    serializer_class = PostsSerializers.ViewPostSerializer
    queryset = PostsModels.ViewPost.objects.all()
