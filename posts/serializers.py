from rest_framework.serializers import (
    ModelSerializer, Serializer
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


class AlbumWithPostSerializer(Serializer):
    """
    Custom serializer for returning an album along with its posts.
    The output format will be a dictionary:
        {
            "album": { ...album data... },
            "posts": [ ...list of post data... ]
        }
    """

    def to_representation(self, instance):
        """
        Convert a tuple (album, posts) into a dictionary representation.

        Steps:
        1. Unpack the tuple into `album` and `posts`.
        2. Serialize the album instance using AlbumsSerializer.
        3. Serialize the list of posts using PostsSerializer with many=True.
        4. Return a dictionary with keys 'album' and 'posts'.
        """
        album, posts = instance  # unpack the tuple
        album_data = AlbumsSerializer(album).data  # serialize the album
        # serialize all related posts
        posts_data = PostsSerializer(posts, many=True).data
        return {
            'album': album_data,  # key 'album' holds serialized album data
            'posts': posts_data   # key 'posts' holds list of serialized posts
        }
