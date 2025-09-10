from rest_framework.serializers import (
    ModelSerializer
)
from users import models as UsersModels
from core.serializers import (
    UsersSerializer,
)
from core.models import Users
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed


class FollowSerializer(ModelSerializer):
    follower_user_details = UsersSerializer(
        read_only=True, source='follower_user'
    )
    followed_user_detials = UsersSerializer(
        read_only=True, source='followed_user'
    )

    class Meta:
        model = UsersModels.Follow
        exclude = ['follower_user']


class LoginsSerializers(ModelSerializer):
    user_details = UsersSerializer(read_only=True, source='user')

    class Meta:
        model = UsersModels.Logins
        fields = '__all__'


class TokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if self.user.status != Users.Status.ACTIVE:
            raise AuthenticationFailed(
                detail=f"Your account is {self.user.status}.",
            )

        return data
