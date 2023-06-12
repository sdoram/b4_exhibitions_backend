from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "users"

urlpatterns = [
    path("signup/", views.UserView.as_view(), name="user-signup"),
    path("signin/", views.CustomTokenObtainPairView.as_view(), name="user-signin"),
    path("", views.UserDetailView.as_view(), name="user-update-and-delete"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("<int:user_id>/", views.UserMypageView.as_view(), name="user-mypage"),
]
