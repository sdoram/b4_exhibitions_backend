from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from users import views

app_name = "users"

urlpatterns = [
    path("signup/", views.UserView.as_view(), name="user-signup"),
    path("signin/", views.CustomTokenObtainPairView.as_view(), name="user-signin"),
    path("", views.UserView.as_view(), name="user-update-and-delete"),
    path("<int:user_id>/", views.UserView.as_view(), name="user-mypage"),
    path("google/", views.GoogleSignin.as_view(), name="google-signin"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
