from decimal import Decimal
from datetime import datetime

from labs.models import Equipment

from .models import (
    LabBooking,
    LabBookingEquipment,
    HallBooking,
)


def is_overlap(
    start1,
    end1,
    start2,
    end2
):

    return (
        start1 < end2
        and
        end1 > start2
    )


def get_duration_hours(
    from_time,
    to_time
):

    start = datetime.combine(
        datetime.today(),
        from_time
    )

    end = datetime.combine(
        datetime.today(),
        to_time
    )

    return Decimal(
        str(
            (end - start).total_seconds() / 3600
        )
    )


def calculate_equipment_fee(
    equipment,
    from_time,
    to_time
):

    hours = get_duration_hours(
        from_time,
        to_time
    )

    return (
        hours *
        equipment.fee_per_hour
    )


def calculate_full_lab_fee(
    lab,
    from_time,
    to_time
):

    total = Decimal("0")

    equipments = Equipment.objects.filter(
        lab=lab
    )

    for equipment in equipments:

        total += calculate_equipment_fee(
            equipment,
            from_time,
            to_time
        )

    return total


def calculate_selected_equipment_fee(
    equipments,
    from_time,
    to_time
):

    total = Decimal("0")

    for equipment in equipments:

        total += calculate_equipment_fee(
            equipment,
            from_time,
            to_time
        )

    return total


def lab_slot_available(
    lab,
    booking_date,
    from_time,
    to_time,
    exclude_booking=None
):

    bookings = LabBooking.objects.filter(
        lab=lab,
        booking_date=booking_date,
        status="APPROVED"
    )

    if exclude_booking:

        bookings = bookings.exclude(
            id=exclude_booking.id
        )

    for booking in bookings:

        if is_overlap(
            from_time,
            to_time,
            booking.from_time,
            booking.to_time
        ):

            return False

    return True


def equipment_slot_available(
    equipment,
    booking_date,
    from_time,
    to_time,
    exclude_booking=None
):

    bookings = LabBookingEquipment.objects.filter(
        equipment=equipment,
        booking__booking_date=booking_date,
        booking__status="APPROVED"
    )

    if exclude_booking:

        bookings = bookings.exclude(
            booking=exclude_booking
        )

    for item in bookings:

        if is_overlap(
            from_time,
            to_time,
            item.from_time,
            item.to_time
        ):

            return False

    return True


def hall_slot_available(
    hall,
    booking_date,
    from_time,
    to_time,
    exclude_booking=None
):

    bookings = HallBooking.objects.filter(
        hall=hall,
        booking_date=booking_date,
        status="APPROVED"
    )

    if exclude_booking:

        bookings = bookings.exclude(
            id=exclude_booking.id
        )

    for booking in bookings:

        if is_overlap(
            from_time,
            to_time,
            booking.from_time,
            booking.to_time
        ):

            return False

    return True


def validate_hall_capacity(
    hall,
    seats
):

    if seats > hall.capacity:

        return (
            False,
            f"Maximum capacity is {hall.capacity}"
        )

    return (
        True,
        ""
    )


def get_lab_booking_colour(
    lab_id
):

    colours = [

        "#D6EAF8",
        "#D5F5E3",
        "#FCF3CF",
        "#FADBD8",
        "#E8DAEF",
        "#FDEDEC",
        "#EBDEF0",
        "#EAFAF1",

    ]

    return colours[
        lab_id % len(colours)
    ]


def get_hall_booking_colour(
    hall_id
):

    colours = [

        "#AED6F1",
        "#A9DFBF",
        "#F9E79F",
        "#F5B7B1",
        "#D2B4DE",
        "#A3E4D7",

    ]

    return colours[
        hall_id % len(colours)
    ]