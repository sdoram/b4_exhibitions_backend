from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("signup/", views.UserView.as_view(), name="user_signup"),
    path("signin/", views.CustomTokenObtainPairView.as_view(), name="user_signin"),
    path("", views.UserDetailView.as_view(), name="user_update_and_delete"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
