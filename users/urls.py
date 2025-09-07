from django.urls import (
    path, include
)
from rest_framework.routers import DefaultRouter
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

router = DefaultRouter()
router.register(r'follow', views.FollowView, basename='follow')
router.register(r'logins', views.LoginsView, basename='logins')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', views.TokenObtianView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('my-followers/', views.MyFollowers.as_view(), name='token_refresh'),
    path('my-followings/', views.MyFollowings.as_view(), name='token_refresh'),
]
