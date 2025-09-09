from rest_framework.serializers import (
    ModelSerializer, CharField
)
from core import models as CoreModels


class UsersSerializer(ModelSerializer):
    password = CharField(write_only=True)

    def create(self, validated_data):
        # pop password and hash it
        password = validated_data.pop("password", None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        # pop password and hash it
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    class Meta:
        model = CoreModels.Users
        fields = '__all__'


class TextsSerializer(ModelSerializer):
    user_detail = UsersSerializer(read_only=True, source='user')

    class Meta:
        model = CoreModels.Texts
        exclude = ['user']


class VideosSerializer(ModelSerializer):
    user_detail = UsersSerializer(read_only=True, source='user')

    class Meta:
        model = CoreModels.Videos
        exclude = ['user']


class ImagesSerializer(ModelSerializer):
    user_detail = UsersSerializer(read_only=True, source='user')

    class Meta:
        model = CoreModels.Images
        exclude = ['user']


class PostsSerializer(ModelSerializer):
    user_detail = UsersSerializer(read_only=True, source='user')
    text_detail = TextsSerializer(read_only=True, source='text')
    video_detail = VideosSerializer(read_only=True, source='video')
    image_detail = ImagesSerializer(read_only=True, source='image')

    class Meta:
        model = CoreModels.Posts
        exclude = ['user']
