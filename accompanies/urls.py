from django.urls import path
from accompanies import views

app_name = "accompanies"

urlpatterns = [
    path("<int:exhibition_id>/", views.AccompanyView.as_view(), name="accompany-view"),
    path(
        "detail/<int:accompany_id>/",
        views.AccompanyView.as_view(),
        name="accompany-view",
    ),
    path("<int:accompany_id>/apply/", views.ApplyView.as_view(), name="apply-view"),
    path("apply/<int:apply_id>/", views.ApplyView.as_view(), name="apply-view"),
    path(
        "<int:accompany_id>/pick/<int:apply_id>/",
        views.AccompanyPickView.as_view(),
        name="accompany-pick-view",
    ),
]
