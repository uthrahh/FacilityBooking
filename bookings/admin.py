from django.contrib import admin

from .models import (
    LabBooking,
    HallBooking,
    LabBookingEquipment,
    BookingHistory
)
from notifications.services import (
    create_notification
)


@admin.register(LabBooking)
class LabBookingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "startup",
        "lab",
        "booking_date",
        "status"
    )

    search_fields = (
        "startup__name",
        "lab__name"
    )

    def save_model(
        self,
        request,
        obj,
        form,
        change
    ):

        if change:

            old = (
                LabBooking.objects.get(
                    id=obj.id
                )
            )

            if (
                old.status
                !=
                obj.status
            ):

                create_notification(
                    startup=obj.startup,
                    title="Lab Booking Updated",
                    message=(
                        f"Booking "
                        f"{obj.id} "
                        f"is now "
                        f"{obj.status}"
                    )
                )


@admin.register(HallBooking)
class HallBookingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "startup",
        "hall",
        "booking_date",
        "status"
    )

    search_fields = (
        "startup__name",
        "hall__name"
    )

    def save_model(
        self,
        request,
        obj,
        form,
        change
    ):

        if change:

            old = (
                HallBooking.objects.get(
                    id=obj.id
                )
            )

            if (
                old.status
                !=
                obj.status
            ):

                create_notification(
                    "Hall Booking Updated",
                    (
                        f"Booking "
                        f"{obj.id} "
                        f"is now "
                        f"{obj.status}"
                    )
                )

        super().save_model(
            request,
            obj,
            form,
            change
        )


admin.site.register(
    LabBookingEquipment
)

admin.site.register(
    BookingHistory
)