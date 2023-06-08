from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("signup/", views.UserView.as_view(), name="user_view"),
    path(
        "signin/", views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path("", views.UserDetailView.as_view(), name="user_detail_view"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
