from django.urls import (
    path, include
)
from rest_framework.routers import DefaultRouter
from users import views

router = DefaultRouter()
router.register(r'follow', views.FollowView, basename='follow')
router.register(r'logins', views.LoginsView, basename='logins')

urlpatterns = [
    path('', include(router.urls)),
]
