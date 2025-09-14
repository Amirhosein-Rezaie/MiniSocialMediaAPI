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
from core.helper import (
    dynamic_search, set_queryset
)
from drf_spectacular.utils import (
    extend_schema, OpenApiParameter
)
from core.permissions import (
    IsAdmin, IsAnonymous, IsSelfOrReadOnly
)


# Users APIs
class UserView(ModelViewSet):
    serializer_class = CoreSerializers.UsersSerializer
    queryset = CoreModels.Users.objects.all()
    permission_classes = [IsSelfOrReadOnly]

    @extend_schema(
        description="""
        Get request of users returns all of the uesrs.
        for search in them and all of fields (foreign, normal) can use queryparmas.
        """,
        parameters=[
            OpenApiParameter(
                name='username', description="An example as normal field in search (?username=a)", required=False,
            ),
            OpenApiParameter(
                name='page', type=int, description="Page number to return.", required=False,
            ),
            OpenApiParameter(
                name='limit', type=int, description="Number of items per page.", required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.status = CoreModels.Users.Status.IS_DELETED
        obj.save()
        return Response(
            data=CoreSerializers.UsersSerializer(obj).data,
            status=status.HTTP_200_OK
        )

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAnonymous()]

        return super().get_permissions()

    def get_queryset(self):
        request = self.request
        if request.query_params:
            return dynamic_search(request, CoreModels.Users)
        return super().get_queryset()


# Texts APIs
class TextsView(GenericViewSet, RetrieveModelMixin, ListModelMixin, CreateModelMixin):
    serializer_class = CoreSerializers.TextsSerializer
    queryset = CoreModels.Texts.objects.all()
    permission_classes = [IsSelfOrReadOnly]

    def get_queryset(self):
        request = self.request
        if request.query_params:
            return dynamic_search(request, CoreModels.Texts)
        return set_queryset(self, CoreModels.Users.Roles.USER, 'user', self.request.user.pk, CoreModels.Texts)

    @extend_schema(
        description="""
        Get request of texts returns all of the texts.
        for search in them and all of fields can use queryparmas.
        """,
        parameters=[
            OpenApiParameter(
                name='text', description="An example as normal field in search (?text=abc)", required=False,
            ),
            OpenApiParameter(
                name='user-id', description="An example as foreign field in search (?user-id=1)", required=False,
            ),
            OpenApiParameter(
                name='page', type=int, description="Page number to return.", required=False,
            ),
            OpenApiParameter(
                name='limit', type=int, description="Number of items per page.", required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)


# Videos APIs
class VideosView(GenericViewSet, RetrieveModelMixin, ListModelMixin, CreateModelMixin):
    serializer_class = CoreSerializers.VideosSerializer
    queryset = CoreModels.Videos.objects.all()
    permission_classes = [IsSelfOrReadOnly]

    def get_permissions(self):
        request = self.request

        if request.method in ['DELETE']:
            return [IsAdmin]

        return super().get_permissions()

    def get_queryset(self):
        request = self.request
        if request.query_params:
            return dynamic_search(request, CoreModels.Videos)
        return set_queryset(self, CoreModels.Users.Roles.USER, 'user', self.request.user.pk, CoreModels.Videos)

    @extend_schema(
        description="""
        Get request of videos returns all of the videos.
        for search in them and all of fields can use queryparmas.
        """,
        parameters=[
            OpenApiParameter(
                name='caption', description="An example as normal field in search (?caption=abc)", required=False,
            ),
            OpenApiParameter(
                name='user-id', description="An example as foreign field in search (?user-id=1)", required=False,
            ),
            OpenApiParameter(
                name='page', type=int, description="Page number to return.", required=False,
            ),
            OpenApiParameter(
                name='limit', type=int, description="Number of items per page.", required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)


# Videos APIs
class ImagesView(GenericViewSet, RetrieveModelMixin, ListModelMixin, CreateModelMixin):
    """
    A view for get and create image
    """
    serializer_class = CoreSerializers.ImagesSerializer
    queryset = CoreModels.Images.objects.all()
    permission_classes = [IsSelfOrReadOnly]

    def get_permissions(self):
        request = self.request

        if request.method in ['DELETE']:
            return [IsAdmin]

        return super().get_permissions()

    def get_queryset(self):
        request = self.request
        if request.query_params:
            return dynamic_search(request, CoreModels.Images)
        return set_queryset(self, CoreModels.Users.Roles.USER, 'user', self.request.user.pk, CoreModels.Images)

    @extend_schema(
        description="""
        Get request of images returns all of the images.
        for search in them and all of fields can use queryparmas.
        """,
        parameters=[
            OpenApiParameter(
                name='caption', description="An example as normal field in search (?caption=abc)", required=False,
            ),
            OpenApiParameter(
                name='user-id', description="An example as foreign field in search (?user-id=1)", required=False,
            ),
            OpenApiParameter(
                name='page', type=int, description="Page number to return.", required=False,
            ),
            OpenApiParameter(
                name='limit', type=int, description="Number of items per page.", required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)


# Posts APIs
class PostsView(ModelViewSet):
    serializer_class = CoreSerializers.PostsSerializer
    queryset = CoreModels.Posts.objects.all()
    permission_classes = [IsSelfOrReadOnly]

    def get_queryset(self):
        request = self.request
        if request.query_params:
            return dynamic_search(request, CoreModels.Posts)
        return set_queryset(self, CoreModels.Users.Roles.USER, 'user', self.request.user.pk, CoreModels.Posts)

    @extend_schema(
        description="""
        Get request of posts returns all of the posts.
        for search in them and all of fields can use queryparmas.
        """,
        parameters=[
            OpenApiParameter(
                name='title', description="An example as normal field in search (?title=abc)", required=False,
            ),
            OpenApiParameter(
                name='user-id', description="An example as foreign field in search (?user-id=1)", required=False,
            ),
            OpenApiParameter(
                name='page', type=int, description="Page number to return.", required=False,
            ),
            OpenApiParameter(
                name='limit', type=int, description="Number of items per page.", required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request: Request, *args, **kwargs):
        # variables
        status_value_IN_USED = CoreModels.Images.Status.IS_USED
        data = request.data
        image = data.get('image')
        video = data.get('video')
        text = data.get('text')
        user = request.user.pk

        # process (validate)
        if image:
            found = CoreModels.Images.objects.get(Q(pk=image))
            if found.user.pk != user:
                return Response(
                    {"detail": f"The uploader of the image ({image}) is not equal to post's uploader ({user}).", },
                    status=status.HTTP_400_BAD_REQUEST
                )

            CoreModels.Images.objects.filter(Q(
                pk=image
            )).update(status=status_value_IN_USED)

        if video:
            found = CoreModels.Videos.objects.get(Q(pk=video))
            if found.user.pk != user:
                return Response(
                    {"detail": f"The uploader of the video ({video}) is not equal to post's uploader ({user}).", },
                    status=status.HTTP_400_BAD_REQUEST
                )

            CoreModels.Videos.objects.filter(Q(
                pk=video
            )).update(status=status_value_IN_USED)

        if text:
            found = CoreModels.Texts.objects.get(Q(pk=text))
            print(found.user.pk)
            if found.user.pk != user:
                return Response(
                    {"detail": f"The uploader of the text ({text}) is not equal to post's uploader ({user}).", },
                    status=status.HTTP_400_BAD_REQUEST
                )

            CoreModels.Texts.objects.filter(Q(
                pk=text
            )).update(status=status_value_IN_USED)

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)
