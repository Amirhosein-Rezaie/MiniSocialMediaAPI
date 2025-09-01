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
        fields = '__all__'


class SavePostSerializer(ModelSerializer):
    user_details = UsersSerializer(read_only=True, source='user')
    post_details = PostsSerializer(read_only=True, source='post')
    album_details = AlbumsSerializer(read_only=True, source='album')

    class Meta:
        model = PostsModels.SavePosts
        fields = '__all__'


class LikePostSerializer(ModelSerializer):
    user_details = UsersSerializer(read_only=True, source='user')
    post_details = PostsSerializer(read_only=True, source='post')

    class Meta:
        model = PostsModels.LikePost
        fields = '__all__'


class CommentsSerializer(ModelSerializer):
    user_details = UsersSerializer(read_only=True, source='user')
    post_details = PostsSerializer(read_only=True, source='post')

    class Meta:
        model = PostsModels.Comments
        fields = '__all__'


class ViewPostSerializer(ModelSerializer):
    user_details = UsersSerializer(read_only=True, source='user')
    post_details = PostsSerializer(read_only=True, source='post')

    class Meta:
        model = PostsModels.ViewPost
        fields = '__all__'
