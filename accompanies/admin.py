from django.contrib import admin
from .models import Accompany, Apply


class ApplyInline(admin.TabularInline):
    model = Apply


@admin.register(Accompany)
class AccompanyAdmin(admin.ModelAdmin):
    list_display = [
        "exhibition",
        "content",
        "user",
        "personnel",
        "start_time",
        "end_time",
    ]
    list_display_links = ["content"]

    inlines = [ApplyInline]
