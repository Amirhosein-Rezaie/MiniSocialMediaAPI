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
from rest_framework.request import Request


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
class TextsView(GenericViewSet, RetrieveModelMixin, ListModelMixin, CreateModelMixin):
    """
    A view for get and create texts
    """
    serializer_class = CoreSerializers.TextsSerializer
    queryset = CoreModels.Texts.objects.all()


# Videos APIs
class VideosView(GenericViewSet, RetrieveModelMixin, ListModelMixin, CreateModelMixin):
    """
    A view for get and create video
    """
    serializer_class = CoreSerializers.VideosSerializer
    queryset = CoreModels.Videos.objects.all()


# Videos APIs
class ImagesView(GenericViewSet, RetrieveModelMixin, ListModelMixin, CreateModelMixin):
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

    def create(self, request: Request, *args, **kwargs):
        # variables
        status_value_IN_USED = CoreModels.Images.Status.IS_USED
        data = request.data
        image = data.get('image')
        video = data.get('video')
        text = data.get('text')
        user = data.get('user')

        # process (validate)
        if image:
            found = CoreModels.Images.objects.get(Q(pk=image))
            if found.user != user:
                return Response(
                    {"detail": f"The uploader of the image ({image}) is not equal to post's uploader ({user}).", },
                    status=status.HTTP_400_BAD_REQUEST
                )

            CoreModels.Images.objects.filter(Q(
                pk=image
            )).update(status=status_value_IN_USED)

        if video:
            found = CoreModels.Videos.objects.get(Q(pk=video))
            if found.user != user:
                return Response(
                    {"detail": f"The uploader of the video ({video}) is not equal to post's uploader ({user}).", },
                    status=status.HTTP_400_BAD_REQUEST
                )

            CoreModels.Videos.objects.filter(Q(
                pk=video
            )).update(status=status_value_IN_USED)

        if text:
            found = CoreModels.Videos.objects.get(Q(pk=text))
            if found.user != user:
                return Response(
                    {"detail": f"The uploader of the text ({text}) is not equal to post's uploader ({user}).", },
                    status=status.HTTP_400_BAD_REQUEST
                )

            CoreModels.Texts.objects.filter(Q(
                pk=text
            )).update(status=status_value_IN_USED)

        return super().create(request, *args, **kwargs)
