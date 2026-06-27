from django.http import JsonResponse

from bookings.models import (
    LabBooking,
    LabBookingEquipment,
    HallBooking,
)

from labs.models import Equipment


def equipment_api(
    request,
    lab_id
):

    booking_date = request.GET.get(
        "date"
    )

    equipments = Equipment.objects.filter(
        lab_id=lab_id
    )

    response = []

    for equipment in equipments:

        occupied = []

        bookings = (
            LabBookingEquipment.objects
            .filter(
                equipment=equipment,
                booking__booking_date=booking_date,
                booking__status="APPROVED"
            )
            .select_related(
                "booking"
            )
        )

        for booking in bookings:

            occupied.append(
                {
                    "from":
                    booking.from_time.strftime(
                        "%H:%M"
                    ),

                    "to":
                    booking.to_time.strftime(
                        "%H:%M"
                    )
                }
            )

        response.append(
            {
                "id":
                equipment.id,

                "equipment_id":
                equipment.equipment_id,

                "name":
                equipment.name,

                "fee":
                float(
                    equipment.fee_per_hour
                ),

                "occupied":
                occupied
            }
        )

    return JsonResponse(
        response,
        safe=False
    )


def lab_availability_api(
    request,
    lab_id
):

    booking_date = request.GET.get(
        "date"
    )

    bookings = LabBooking.objects.filter(
        lab_id=lab_id,
        booking_date=booking_date,
        status="APPROVED"
    )

    response = []

    for booking in bookings:

        if (
            booking.from_time
            and
            booking.to_time
        ):

            response.append(
                {
                    "from":
                    booking.from_time.strftime(
                        "%H:%M"
                    ),

                    "to":
                    booking.to_time.strftime(
                        "%H:%M"
                    ),

                    "booking_id":
                    booking.id
                }
            )

    return JsonResponse(
        response,
        safe=False
    )


def hall_availability_api(
    request,
    hall_id
):

    booking_date = request.GET.get(
        "date"
    )

    bookings = HallBooking.objects.filter(
        hall_id=hall_id,
        booking_date=booking_date,
        status="APPROVED"
    )

    response = []

    for booking in bookings:

        response.append(
            {
                "from":
                booking.from_time.strftime(
                    "%H:%M"
                ),

                "to":
                booking.to_time.strftime(
                    "%H:%M"
                ),

                "booking_id":
                booking.id
            }
        )

    return JsonResponse(
        response,
        safe=False
    )


def calendar_events(
    request
):

    events = []

    lab_colors = [

        "#D6EAF8",

        "#D5F5E3",

        "#FCF3CF",

        "#FADBD8",

        "#E8DAEF",

        "#FDEDEC",

        "#EBDEF0",

        "#EAFAF1",

    ]

    hall_colors = [

        "#AED6F1",

        "#A9DFBF",

        "#F9E79F",

        "#F5B7B1",

        "#D2B4DE",

        "#A3E4D7",

    ]

    lab_bookings = LabBooking.objects.filter(
        status="APPROVED"
    ).select_related(
        "lab"
    )

    for booking in lab_bookings:

        if (
            not booking.from_time
            or
            not booking.to_time
        ):
            continue

        events.append(
            {

                "id":
                f"lab-{booking.id}",

                "booking_id":
                booking.id,

                "title":
                booking.lab.name,

                "start":
                f"{booking.booking_date}T{booking.from_time}",

                "end":
                f"{booking.booking_date}T{booking.to_time}",

                "color":
                lab_colors[
                    booking.lab.id %
                    len(lab_colors)
                ]

            }
        )

    hall_bookings = HallBooking.objects.filter(
        status="APPROVED"
    ).select_related(
        "hall"
    )

    for booking in hall_bookings:

        events.append(
            {

                "id":
                f"hall-{booking.id}",

                "booking_id":
                booking.id,

                "title":
                booking.hall.name,

                "start":
                f"{booking.booking_date}T{booking.from_time}",

                "end":
                f"{booking.booking_date}T{booking.to_time}",

                "color":
                hall_colors[
                    booking.hall.id %
                    len(hall_colors)
                ]

            }
        )

    return JsonResponse(
        events,
        safe=False
    )