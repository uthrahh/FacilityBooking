from django.contrib import admin

from .models import (
    LabBooking,
    HallBooking,
    LabBookingEquipment,
    BookingHistory,
)


@admin.register(LabBooking)
class LabBookingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "startup",
        "lab",
        "booking_date",
        "status",
    )

    search_fields = (
        "startup__name",
        "lab__name",
    )


@admin.register(HallBooking)
class HallBookingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "startup",
        "hall",
        "booking_date",
        "status",
    )

    search_fields = (
        "startup__name",
        "hall__name",
    )


admin.site.register(LabBookingEquipment)

admin.site.register(BookingHistory)