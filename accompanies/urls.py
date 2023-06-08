from django.urls import path
from accompanies import views

urlpatterns = [
    path("<int:exhibition_id>/", views.AccompanyView.as_view(), name="accompany_view"),
]
