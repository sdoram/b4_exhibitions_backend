from django.urls import path
from .views import ExhibitionView, ExhibitionDetailView, ExhibitionLikeView

urlpatterns = [
    path("", ExhibitionView.as_view(), name="exhibition"),
    path("<int:exhibitions_id>/", ExhibitionDetailView.as_view(), name="exhibition-detail"),
    path("<int:exhibitions_id>/like/", ExhibitionLikeView.as_view(), name="exhibition-like"),
]
