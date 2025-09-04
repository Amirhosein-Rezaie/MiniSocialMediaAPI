from rest_framework.viewsets import (
    ModelViewSet, GenericViewSet,
)
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin
)
from posts import serializers as PostsSerializers
from posts import models as PostsModels
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status as Status
from core.helper import (dynamic_search)
from rest_framework.request import Request
from drf_spectacular.utils import (
    extend_schema, OpenApiParameter
)


# Albums APIs
class AlbumsView(ModelViewSet):
    serializer_class = PostsSerializers.AlbumsSerializer
    queryset = PostsModels.Albums.objects.all()

    @extend_schema(
        description="""
        Get request of users returns all of the Albums.
        for search in them and all of fields (foreign, normal) can use queryparmas.
        """,
        parameters=[
            OpenApiParameter(
                name='title', description="An example as normal field in search (?title=abc)", required=False,
            ),
            OpenApiParameter(
                name='user-id', description="An example as foreign field in search (?user-id=1)", required=False,
            ),
        ]
    )
    def list(self, request: Request, *args, **kwargs):
        if request.query_params:
            return dynamic_search(self, request, PostsModels.Albums)
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description="can change only title. in update request."
    )
    def update(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        update_field_value = request.data.get('title')

        if update_field_value is None:
            return Response({"detail": "title is required"}, status=Status.HTTP_400_BAD_REQUEST,)

        instance.title = update_field_value
        instance.save(update_fields=['title'])
        return Response(PostsSerializers.AlbumsSerializer(instance).data, status=Status.HTTP_200_OK)


# SavePosts APIs
class SavePostsView(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin):
    serializer_class = PostsSerializers.SavePostSerializer
    queryset = PostsModels.SavePosts.objects.all()

    @extend_schema(
        description="""
        Get request of users returns all of the SavePosts.
        for search in them and all of fields (foreign, normal) can use queryparmas.
        """,
        parameters=[
            OpenApiParameter(
                name='user-id', description="An example as foreign field in search (?user-id=1)", required=False,
            ),
        ]
    )
    def list(self, request: Request, *args, **kwargs):
        if request.query_params:
            return dynamic_search(self, request, PostsModels.SavePosts)
        return super().list(request, *args, **kwargs)

    def create(self, request: Request, *args, **kwargs):
        """
        This request is for save posts by users.
        """
        # varibles
        data = request.data
        user = data.get('user')
        post = data.get('post')
        album = data.get('album')

        # process (validate)
        if user and post and album:
            found_album = PostsModels.Albums.objects.filter(Q(
                user=user, id=album
            ))
            if not found_album:
                return Response(
                    {"detail": f"This album({album}) is not owned by this user({user})"},
                    status=Status.HTTP_400_BAD_REQUEST
                )
            found = PostsModels.SavePosts.objects.filter(Q(
                user=user, post=post, album=album
            ))
            if found:
                return Response(
                    {"detail": f"This post({post}) has been saved by this user({user}) in this album({album})."},
                    status=Status.HTTP_400_BAD_REQUEST
                )

        return super().create(request, *args, **kwargs)


# LikePost APIs
class LikePostView(ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = PostsSerializers.LikePostSerializer
    queryset = PostsModels.LikePost.objects.all()

    @extend_schema(
        description="""
        Get request of users returns all of the LikePost.
        for search in them and all of fields (foreign, normal) can use queryparmas.
        """,
        parameters=[
            OpenApiParameter(
                name='user-id', description="An example as foreign field in search (?user-id=1)", required=False,
            ),
        ]
    )
    def list(self, request: Request, *args, **kwargs):
        if request.query_params:
            return dynamic_search(self, request, PostsModels.LikePost)
        return super().list(request, *args, **kwargs)

    def create(self, request: Request, *args, **kwargs):
        data = request.data
        user = data.get('user')
        post = data.get('post')

        if user and post:
            found_like = PostsModels.LikePost.objects.filter(Q(
                user=user, post=post
            ))

            if found_like:
                return Response(
                    {"detail": f"This user({user}) have liked this ({post})."},
                    status=Status.HTTP_400_BAD_REQUEST
                )

        return super().create(request, *args, **kwargs)


# Comments APIs
class CommentsView(ModelViewSet):
    serializer_class = PostsSerializers.CommentsSerializer
    queryset = PostsModels.Comments.objects.all()

    @extend_schema(
        description="""
        Get request of users returns all of the Comments.
        for search in them and all of fields (foreign, normal) can use queryparmas.
        """,
        parameters=[
            OpenApiParameter(
                name='comment', description="An example as normal field in search (?comment=abc)", required=False,
            ),
            OpenApiParameter(
                name='user-id', description="An example as foreign field in search (?user-id=1)", required=False,
            ),
        ]
    )
    def list(self, request: Request, *args, **kwargs):
        if request.query_params:
            return dynamic_search(self, request, PostsModels.Comments)
        return super().list(request, *args, **kwargs)

    def update(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        update_field_value = request.data.get('comment')

        if update_field_value is None:
            return Response({"detail": "comment is required"}, status=Status.HTTP_400_BAD_REQUEST,)

        instance.comment = update_field_value
        instance.save(update_fields=['comment'])
        return Response(PostsSerializers.CommentsSerializer(instance).data, status=Status.HTTP_200_OK)


class ViewPostView(ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = PostsSerializers.ViewPostSerializer
    queryset = PostsModels.ViewPost.objects.all()

    @extend_schema(
        description="""
        Get request of users returns all of the ViewPost.
        for search in them and all of fields (foreign, normal) can use queryparmas.
        """,
        parameters=[
            OpenApiParameter(
                name='user-id', description="An example as foreign field in search (?user-id=1)", required=False,
            ),
        ]
    )
    def list(self, request: Request, *args, **kwargs):
        if request.query_params:
            return dynamic_search(self, request, PostsModels.ViewPost)
        return super().list(request, *args, **kwargs)

    def create(self, request: Request, *args, **kwargs):
        data = request.data
        user = data.get('user')
        post = data.get('post')

        if user and post:
            found_view = PostsModels.ViewPost.objects.filter(
                Q(user=user, post=post)
            )
            if found_view:
                return Response(
                    {"detail": f"This user({user}) have seen this ({post})."},
                    status=Status.HTTP_200_OK
                )
            else:
                return super().create(request, *args, **kwargs)
        else:
            return Response(
                {"detail": "user and post are required."},
                status=Status.HTTP_400_BAD_REQUEST
            )
