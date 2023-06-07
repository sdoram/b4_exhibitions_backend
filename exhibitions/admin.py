from django.contrib import admin
from .models import Exhibition


@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ("info_name", "period", "location", "created_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("info_name", "content", "location")
