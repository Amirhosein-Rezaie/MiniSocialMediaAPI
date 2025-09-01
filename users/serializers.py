from rest_framework.serializers import (
    ModelSerializer
)
from users import models as UsersModels
from core.serializers import (
    UsersSerializer,
)


class Follow(ModelSerializer):
    follower_user_details = UsersSerializer(
        read_only=True, source='follower_user'
    )
    followed_user_detials = UsersSerializer(
        read_only=True, source='followed_user'
    )

    class Meta:
        model = UsersModels.Follow
        fields = '__all__'


class Follow(ModelSerializer):
    user_details = UsersSerializer(read_only=True, source='user')

    class Meta:
        model = UsersModels.Logins
        fields = '__all__'
