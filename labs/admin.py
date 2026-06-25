from django.contrib import admin
from .models import Lab, Equipment


@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):

    list_display = (
        "lab_id",
        "name",
    )


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):

    list_display = (
        "equipment_id",
        "name",
        "lab",
        "fee_per_hour",
    )