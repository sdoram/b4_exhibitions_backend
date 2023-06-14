from django.urls import path
from exhibitions import views

app_name = "exhibitions"

urlpatterns = [
    path("", views.ExhibitionView.as_view(), name="exhibition"),

    path("search/", views.ExhibitionSearchView.as_view(), name="search"),
    path(
        "<int:exhibition_id>/",
        views.ExhibitionDetailView.as_view(),
        name="exhibition-detail",
    ),
    path(
        "<int:exhibition_id>/like/",
        views.ExhibitionLikeView.as_view(),
        name="exhibition-like",
    ),
]
