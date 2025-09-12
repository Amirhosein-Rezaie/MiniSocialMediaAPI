from django.urls import (
    path, include
)
from rest_framework.routers import DefaultRouter
from posts import views

router = DefaultRouter()
router.register(r'albums', views.AlbumsView, basename='albums')
router.register(r'save-posts', views.SavePostsView, basename='save-posts')
router.register(r'like-posts', views.LikePostView, basename='like-posts')
router.register(r'comments', views.CommentsView, basename='comments')
router.register(r'view-post', views.ViewPostView, basename='view-post')
router.register(r'commented-posts', views.CommentedPosts, basename='commented-posts')
router.register(r'liked-posts', views.LikedPosts, basename='liked-posts')
router.register(r'visited-posts', views.VisitedPosts, basename='visited-posts')
router.register(r'saved-posts', views.SavedPosts, basename='saved-posts')
router.register(r'album-with-posts', views.AlbumWithPosts, basename='album-with-posts')
router.register(r'home', views.Home, basename='home')

urlpatterns = [
    path('', include(router.urls)),
]
