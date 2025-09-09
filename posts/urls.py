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

urlpatterns = [
    path('', include(router.urls)),
    path('liked-posts-user/', views.LikedPostsUser.as_view(), name='liked-posts-user'),
]
