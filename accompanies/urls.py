from django.urls import path
from accompanies import views

app_name = "accompanies"

urlpatterns = [
    path("<int:exhibition_id>/", views.AccompanyView.as_view(), name="accompany"),
    path(
        "detail/<int:accompany_id>/",
        views.AccompanyView.as_view(),
        name="accompany-detail",
    ),
    path("<int:accompany_id>/apply/", views.ApplyView.as_view(), name="apply"),
    path("apply/<int:apply_id>/", views.ApplyView.as_view(), name="apply-detail"),
    path(
        "<int:accompany_id>/pick/<int:apply_id>/",
        views.AccompanyPickView.as_view(),
        name="accompany-pick",
    ),
]
