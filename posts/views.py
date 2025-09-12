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
from core.helper import (
    dynamic_search, set_queryset
)
from rest_framework.request import Request
from drf_spectacular.utils import (
    extend_schema, OpenApiParameter
)
from core.permissions import (IsActive, IsSelfOrReadOnly, IsUser)
from core.models import (
    Users, Posts
)
from core.serializers import (
    PostsSerializer
)
from users.models import Follow
from random import sample


# Albums APIs
class AlbumsView(ModelViewSet):
    serializer_class = PostsSerializers.AlbumsSerializer
    queryset = PostsModels.Albums.objects.all()
    permission_classes = [IsSelfOrReadOnly]

    def get_permissions(self):
        request = self.request

        if request.method in ['POST', 'DELETE', 'UPDATE']:
            return [IsUser()]

        return super().get_permissions()

    def get_queryset(self):
        return set_queryset(self, Users.Roles.USER, 'user', self.request.user.pk, PostsModels.Albums)

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
            OpenApiParameter(
                name='page', type=int, description="Page number to return.", required=False,
            ),
            OpenApiParameter(
                name='limit', type=int, description="Number of items per page.", required=False,
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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)


# SavePosts APIs
class SavePostsView(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin):
    serializer_class = PostsSerializers.SavePostSerializer
    queryset = PostsModels.SavePosts.objects.all()

    def get_permissions(self):
        request = self.request

        if request.method in ['POST', 'DELETE']:
            return [IsUser()]

        return super().get_permissions()

    def get_queryset(self):
        return set_queryset(self, Users.Roles.USER, 'user', self.request.user.pk, PostsModels.SavePosts)

    @extend_schema(
        description="""
        Get request of users returns all of the SavePosts.
        for search in them and all of fields (foreign, normal) can use queryparmas.
        """,
        parameters=[
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
        user = request.user.pk
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

            # check post not to save in same album by the user
            found = PostsModels.SavePosts.objects.filter(Q(
                user=user, post=post, album=album
            )).exists()
            if found:
                return Response(
                    {"detail": f"This post({post}) has been saved by this user({user}) in this album({album})."},
                    status=Status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"detail": "No Parameter."}, status=Status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)


# LikePost APIs
class LikePostView(ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = PostsSerializers.LikePostSerializer
    queryset = PostsModels.LikePost.objects.all()

    def get_queryset(self):
        return set_queryset(self, Users.Roles.USER, 'user', self.request.user.pk, PostsModels.LikePost)

    def get_permissions(self):
        request = self.request

        if request.method in ['POST', 'DELETE',]:
            return [IsUser()]

        return super().get_permissions()

    @extend_schema(
        description="""
        Get request of users returns all of the LikePost.
        for search in them and all of fields (foreign, normal) can use queryparmas.
        """,
        parameters=[
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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)


# Comments APIs
class CommentsView(ModelViewSet):
    serializer_class = PostsSerializers.CommentsSerializer
    queryset = PostsModels.Comments.objects.all()

    def get_queryset(self):
        return set_queryset(self, Users.Roles.USER, 'user', self.request.user.pk, PostsModels.Comments)

    def get_permissions(self):
        request = self.request

        if request.method in ['POST', 'DELETE', 'UPDATE']:
            return [IsUser()]

        return super().get_permissions()

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
            OpenApiParameter(
                name='page', type=int, description="Page number to return.", required=False,
            ),
            OpenApiParameter(
                name='limit', type=int, description="Number of items per page.", required=False,
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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)


class ViewPostView(ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = PostsSerializers.ViewPostSerializer
    queryset = PostsModels.ViewPost.objects.all()

    def get_permissions(self):
        request = self.request

        if request.method in ['POST']:
            return [IsUser()]

        return super().get_permissions()

    def get_queryset(self):
        return set_queryset(self, Users.Roles.USER, 'user', self.request.user.pk, PostsModels.ViewPost)

    @extend_schema(
        description="""
        Get request of users returns all of the ViewPost.
        for search in them and all of fields (foreign, normal) can use queryparmas.
        """,
        parameters=[
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
    def list(self, request: Request, *args, **kwargs):
        if request.query_params:
            return dynamic_search(self, request, PostsModels.ViewPost)
        return super().list(request, *args, **kwargs)

    def create(self, request: Request, *args, **kwargs):
        data = request.data
        user = request.user.pk
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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='page', type=int, description="Page number to return.", required=False,
        ),
        OpenApiParameter(
            name='limit', type=int, description="Number of items per page.", required=False,
        ),
    ],
    responses=PostsSerializer(many=True)
)
class LikedPosts(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    API endpoint that returns a paginated list of posts liked by the current user.

    - Requires the user to be authenticated with `IsUser` permission.
    - Retrieves all posts that the current user has liked.
    - Supports dynamic pagination based on request parameters.
    """
    permission_classes = [IsUser]
    serializer_class = PostsSerializer

    def get_queryset(self):
        user = self.request.user

        # Get all posts that the current user has liked
        posts = Posts.objects.filter(
            Q(id__in=PostsModels.LikePost.objects.filter(
                Q(user=user.pk)
            ).values_list('post', flat=True))
        )
        return posts


# posts that are commented by the authenticated by user
@extend_schema(
    description="An API that returns the posts that commented by the authenticated user.",
    parameters=[
        OpenApiParameter(
            name='page', type=int, description="Page number to return.", required=False,
        ),
        OpenApiParameter(
            name='limit', type=int, description="Number of items per page.", required=False,
        ),
    ],
    responses=PostsSerializer(many=True)
)
class CommentedPosts(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = PostsSerializer
    permission_classes = [IsUser]

    def get_queryset(self):
        request = self.request

        posts = Posts.objects.filter(
            Q(id__in=PostsModels.Comments.objects.filter(
                Q(user=request.user.pk)
            ).values_list('post', flat=True))
        )

        return posts


# posts that are visited by the authenticated by user
@extend_schema(
    description="An API that returns the posts that visited by the authenticated user.",
    parameters=[
        OpenApiParameter(
            name='page', type=int, description="Page number to return.", required=False,
        ),
        OpenApiParameter(
            name='limit', type=int, description="Number of items per page.", required=False,
        ),
    ],
    responses=PostsSerializer(many=True)
)
class VisitedPosts(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = [IsUser]
    serializer_class = PostsSerializer

    def get_queryset(self):
        request = self.request

        return Posts.objects.filter(
            Q(id__in=PostsModels.ViewPost.objects.filter(
                Q(user=request.user.id)
            ).values_list('post', flat=True))
        )


# posts that are saved by the authenticated by user
@extend_schema(
    description="An API that returns the posts that saved by the authenticated user.",
    parameters=[
        OpenApiParameter(
            name='page', type=int, description="Page number to return.", required=False,
        ),
        OpenApiParameter(
            name='limit', type=int, description="Number of items per page.", required=False,
        ),
    ],
    responses=PostsSerializer(many=True)
)
class SavedPosts(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = PostsSerializer
    permission_classes = [IsUser]

    def get_queryset(self):
        request = self.request

        return Posts.objects.filter(
            Q(id__in=PostsModels.SavePosts.objects.filter(
                Q(user=request.user.pk)
            ).values_list('post', flat=True))
        ).distinct()


# album with posts are saved in it
class AlbumWithPosts(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = PostsSerializers.AlbumWithPostSerializer
    permission_classes = [IsUser]

    def get_queryset(self):
        # set queryset as album are created by auth user
        request = self.request
        return PostsModels.Albums.objects.filter(Q(user=request.user.pk))

    def get_serializer(self, *args, **kwargs):
        # This allows passing a tuple (album, posts) directly to the serializer.
        return self.serializer_class(*args, **kwargs)

    @extend_schema(
        description="Returns One album with posts are saved in it by authenticated user.",
    )
    def retrieve(self, request, *args, **kwargs):
        album = self.get_object()  # fetch the album instance
        posts = Posts.objects.filter(
            Q(id__in=PostsModels.SavePosts.objects.filter(
                Q(album=album)).values_list('post', flat=True)
              )
        )  # fetch related posts
        return Response(
            self.serializer_class((album, posts)).data,
            status=Status.HTTP_200_OK
        )

    @extend_schema(
        description="Returns One album with posts are saved in it by authenticated user.",
        parameters=[
            OpenApiParameter(
                name='page', type=int, description="Page number to return.", required=False,
            ),
            OpenApiParameter(
                name='limit', type=int, description="Number of items per page.", required=False,
            ),
        ],
        responses=PostsSerializer(many=True)
    )
    def list(self, request, *args, **kwargs):
        albums = self.get_queryset()  # get album queryset
        data = []  # initialize list to hold serialized results

        for album in albums:
            # Get all posts linked to this album via SavePosts relation
            posts = Posts.objects.filter(
                Q(id__in=PostsModels.SavePosts.objects.filter(
                    Q(album=album)).values_list('post', flat=True))
            )
            # Serialize the album and posts as a tuple and append to data
            data.append(self.serializer_class((album, posts)).data)

        return Response(data, status=Status.HTTP_200_OK)


# home view
@extend_schema(
    description="Returns random posts that are uploaded by users are followed by auth user.",
    parameters=[
        OpenApiParameter(
            name='page', type=int, description="Page number to return.", required=False,
        ),
        OpenApiParameter(
            name='limit', type=int, description="Number of items per page.", required=False,
        ),
    ],
    responses=PostsSerializer(many=True)
)
class RandomPostsFollowingUser(ListModelMixin, GenericViewSet):
    serializer_class = PostsSerializer
    permission_classes = [IsUser]

    def get_queryset(self):
        request = self.request

        following_users = Users.objects.filter(
            Q(id__in=Follow.objects.filter(
                Q(follower_user=request.user.pk)
            ).values_list('followed_user', flat=True))
        )

        return Posts.objects.filter(
            Q(user__id__in=following_users)
        ).order_by('?')
