from rest_framework.serializers import (
    ModelSerializer, CharField
)
from core import models as CoreModels


class UsersSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = CoreModels.Users
        fields = '__all__'


class TextsSerializer(ModelSerializer):
    user_detail = UsersSerializer(read_only=True, source='user')

    class Meta:
        model = CoreModels.Texts
        fields = '__all__'


class VideosSerializer(ModelSerializer):
    user_detail = UsersSerializer(read_only=True, source='user')

    class Meta:
        model = CoreModels.Videos
        fields = '__all__'


class ImagesSerializer(ModelSerializer):
    user_detail = UsersSerializer(read_only=True, source='user')

    class Meta:
        model = CoreModels.Images
        fields = '__all__'


class PostsSerializer(ModelSerializer):
    user_detail = UsersSerializer(read_only=True, source='user')
    text_detail = TextsSerializer(read_only=True, source='text')
    video_detail = VideosSerializer(read_only=True, source='video')
    image_detail = ImagesSerializer(read_only=True, source='image')

    class Meta:
        model = CoreModels.Posts
        fields = '__all__'
