from django.urls import path
from reviews import views

app_name = "reviews"

urlpatterns = [
    path("<int:exhibition_id>/", views.ReviewView.as_view(), name="review"),
    path("detail/<int:review_id>/", views.ReviewView.as_view(), name="review-detail"),
]
