from django.http import JsonResponse

from labs.models import Equipment

from .models import (
    LabBooking,
    HallBooking,
    LabBookingEquipment
)


def equipment_api(
    request,
    lab_id
):

    data = list(
        Equipment.objects.filter(
            lab_id=lab_id
        ).values(
            "id",
            "name",
            "fee_per_hour"
        )
    )

    return JsonResponse(
        data,
        safe=False
    )


def lab_availability_api(
    request,
    lab_id
):

    bookings = (
        LabBooking.objects.filter(
            lab_id=lab_id,
            status="APPROVED"
        )
        .values(
            "booking_date",
            "from_time",
            "to_time"
        )
    )

    data = []

    for booking in bookings:

        data.append(
            {
                "date":
                booking["booking_date"],

                "from":
                booking["from_time"],

                "to":
                booking["to_time"]
            }
        )

    return JsonResponse(
        data,
        safe=False
    )


def hall_availability_api(
    request,
    hall_id
):

    bookings = (
        HallBooking.objects.filter(
            hall_id=hall_id,
            status="APPROVED"
        )
        .values(
            "booking_date",
            "from_time",
            "to_time"
        )
    )

    data = []

    for booking in bookings:

        data.append(
            {
                "date":
                booking["booking_date"],

                "from":
                booking["from_time"],

                "to":
                booking["to_time"]
            }
        )

    return JsonResponse(
        data,
        safe=False
    )