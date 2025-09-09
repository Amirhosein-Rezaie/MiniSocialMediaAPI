from rest_framework.serializers import (
    ModelSerializer
)
from posts import models as PostsModels
from core.serializers import (
    UsersSerializer, PostsSerializer
)


class AlbumsSerializer(ModelSerializer):
    user_details = UsersSerializer(read_only=True, source='user')

    class Meta:
        model = PostsModels.Albums
        exclude = ['user']


class SavePostSerializer(ModelSerializer):
    user_details = UsersSerializer(read_only=True, source='user')
    post_details = PostsSerializer(read_only=True, source='post')
    album_details = AlbumsSerializer(read_only=True, source='album')

    class Meta:
        model = PostsModels.SavePosts
        exclude = ['user']


class LikePostSerializer(ModelSerializer):
    user_details = UsersSerializer(read_only=True, source='user')
    post_details = PostsSerializer(read_only=True, source='post')

    class Meta:
        model = PostsModels.LikePost
        exclude = ['user']


class CommentsSerializer(ModelSerializer):
    user_details = UsersSerializer(read_only=True, source='user')
    post_details = PostsSerializer(read_only=True, source='post')

    class Meta:
        model = PostsModels.Comments
        exclude = ['user']


class ViewPostSerializer(ModelSerializer):
    user_details = UsersSerializer(read_only=True, source='user')
    post_details = PostsSerializer(read_only=True, source='post')

    class Meta:
        model = PostsModels.ViewPost
        exclude = ['user']
