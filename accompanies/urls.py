from django.urls import path
from accompanies import views

urlpatterns = [
    path("<int:exhibition_id>/", views.AccompanyView.as_view(), name="accompany_view"),
    path(
        "detail/<int:accompany_id>/",
        views.AccompanyView.as_view(),
        name="accompany_view",
    ),
    path("<int:accompany_id>/apply/", views.ApplyView.as_view(), name="apply_view"),
    path("apply/<int:apply_id>/", views.ApplyView.as_view(), name="apply_view"),
]
