from django.urls import (
    path, include
)
from rest_framework.routers import DefaultRouter
from posts import views

router = DefaultRouter()
router.register(r'albums', views.AlbumsView, 'albums')
router.register(r'save-posts', views.SavePostsView, 'save-posts')
router.register(r'like-posts', views.LikePostView, 'like-posts')
router.register(r'comments', views.CommentsView, 'comments')
router.register(r'view-post', views.ViewPostView, 'view-post')
router.register(r'commented-posts', views.CommentedPosts, 'commented-posts')
router.register(r'liked-posts', views.LikedPosts, 'liked-posts')
router.register(r'visited-posts', views.VisitedPosts, 'visited-posts')
router.register(r'saved-posts', views.SavedPosts, 'saved-posts')
router.register(r'album-with-posts', views.AlbumWithPosts, 'album-with-posts')
router.register(r'random-posts-following',views.RandomPostsFollowingUser, 'random-posts-following')

urlpatterns = [
    path('', include(router.urls)),
]
