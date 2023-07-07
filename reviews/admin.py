from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        "exhibition",
        "content",
        "user",
    ]
    list_display_links = ["content"]
