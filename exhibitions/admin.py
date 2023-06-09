from django.contrib import admin
from .models import Exhibition
from accompanies.models import Accompany


class AccompanyInline(admin.TabularInline):
    model = Accompany
    readonly_fields = (
        "content",
        "user",
        "personnel",
        "start_time",
        "end_time",
    )
    show_change_link = True


@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = [
        "category",
        "info_name",
        "location",
        "start_time",
        "end_time",
    ]
    list_display_links = ["info_name"]

    inlines = [AccompanyInline]


# admin.site.register(Exhibition)
