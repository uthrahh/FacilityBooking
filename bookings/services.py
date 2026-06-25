from datetime import datetime
from datetime import timedelta

from .models import (
    LabBooking,
    LabBookingEquipment,
    HallBooking,
    BookingHistory
)


def time_overlap(
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


def create_history(
    booking_type,
    booking_id,
    old_status,
    new_status,
    remarks=""
):

    BookingHistory.objects.create(
        booking_type=booking_type,
        booking_id=booking_id,
        old_status=old_status,
        new_status=new_status,
        remarks=remarks
    )


def validate_lab_booking(
    lab,
    equipments,
    booking_date,
    from_time,
    to_time,
    is_full_lab=False
):

    if from_time >= to_time:

        return (
            False,
            "End time must be after start time."
        )

    existing = (
        LabBooking.objects.filter(
            lab=lab,
            booking_date=booking_date
        )
        .exclude(
            status="CANCELLED"
        )
        .exclude(
            status="REJECTED"
        )
    )

    for booking in existing:

        if time_overlap(
            from_time,
            to_time,
            booking.from_time,
            booking.to_time
        ):

            return (
                False,
                "Selected slot unavailable."
            )

    return (
        True,
        "Valid"
    )

def validate_hall_booking(
    hall,
    booking_date,
    from_time,
    to_time
):

    existing = HallBooking.objects.filter(
        hall=hall,
        booking_date=booking_date
    )

    for booking in existing:

        if time_overlap(
            from_time,
            to_time,
            booking.from_time,
            booking.to_time
        ):
            return False, (
                "Hall already booked."
            )

    return True, "Valid"