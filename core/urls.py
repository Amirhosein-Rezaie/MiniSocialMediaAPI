from django.urls import (
    path, include
)
from rest_framework.routers import DefaultRouter
from core import views


router = DefaultRouter()
router.register(r'users', views.UserView, basename='users')
router.register(r'posts', views.PostsView, basename='posts')
router.register(r'texts', views.TextsView, basename='texts')
router.register(r'videos', views.VideosView, basename='videos')
router.register(r'images', views.ImagesView, basename='images')

urlpatterns = [
    path('', include(router.urls)),
]
