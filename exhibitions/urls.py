from django.urls import path
from .views import ExhibitionView, ExhibitionDetailView, ExhibitionLikeView

urlpatterns = [
    path("exhibitions/", ExhibitionView.as_view(), name="exhibition"),
    path("exhibitions/<int:pk>/", ExhibitionDetailView.as_view(), name="exhibition-detail"),
    path("exhibitions/<int:pk>/like/", ExhibitionLikeView.as_view(), name="exhibition-like"),
]
