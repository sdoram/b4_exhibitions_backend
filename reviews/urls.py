from django.urls import path
from .views import ReviewView, ReviewDetailView

urlpatterns = [
    path("<int:exhibitions_id>/", ReviewView.as_view(), name="review"),
    path(
        "detail/<int:exhibitions_id>/", ReviewDetailView.as_view(), name="review-detail"
    ),
]
