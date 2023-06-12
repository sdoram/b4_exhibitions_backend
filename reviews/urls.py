from django.urls import path
from .views import ReviewView, ReviewDetailView

app_name = "reviews"

urlpatterns = [
    path("<int:exhibition_id>/", ReviewView.as_view(), name="review"),
    path("detail/<int:review_id>/", ReviewDetailView.as_view(), name="review-detail"),
]
