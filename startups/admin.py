from django.contrib import admin

from .models import Startup


@admin.register(Startup)
class StartupAdmin(admin.ModelAdmin):

    list_display = (
        "startup_id",
        "name",
        "email",
        "phone",
        "is_active",
    )

    search_fields = (
        "startup_id",
        "name",
        "email",
    )

    list_filter = (
        "is_active",
    )

    ordering = (
        "startup_id",
    )