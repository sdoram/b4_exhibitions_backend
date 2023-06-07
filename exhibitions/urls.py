from django.urls import path
from .views import ExhibitionView, ExhibitionDetailView, ExhibitionLikeView

app_name = "exhibition"

urlpatterns = [
    path("", ExhibitionView.as_view(), name="exhibition"),
    path("<int:exhibition_id>/", ExhibitionDetailView.as_view(), name="exhibition-detail"),
    path("<int:exhibition_id>/like/", ExhibitionLikeView.as_view(), name="exhibition-like"),
]
