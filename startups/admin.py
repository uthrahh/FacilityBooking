from django.contrib import admin

from .models import Startup


@admin.register(Startup)
class StartupAdmin(admin.ModelAdmin):

    list_display = (
        "startup_id",
        "name",
        "founder_name",
        "email",
        "phone",
        "incubation_status",
        "is_active"
    )

    search_fields = (
        "startup_id",
        "name"
    )