from datetime import datetime

from labs.models import Equipment
from .models import (
    LabBooking,
    LabBookingEquipment,
    HallBooking,
    BookingHistory,
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


def validate_lab_booking(

    lab,

    equipments,

    booking_date,

    from_time,

    to_time,

    full_lab=False

):

    if from_time >= to_time:

        return (

            False,

            "Invalid time slot."

        )

    approved = LabBooking.objects.filter(

        lab=lab,

        booking_date=booking_date,

        status="APPROVED"

    )

    for booking in approved:

        if (

            booking.from_time

            and

            booking.to_time

            and

            is_overlap(

                from_time,

                to_time,

                booking.from_time,

                booking.to_time

            )

        ):

            return (

                False,

                "Lab already booked for the selected slot."

            )

    if not full_lab:

        for equipment in equipments:

            existing = LabBookingEquipment.objects.filter(

                equipment=equipment,

                booking__booking_date=booking_date,

                booking__status="APPROVED"

            )

            for item in existing:

                if is_overlap(

                    from_time,

                    to_time,

                    item.from_time,

                    item.to_time

                ):

                    return (

                        False,

                        f"{equipment.name} is unavailable."

                    )

    return (

        True,

        ""

    )


def validate_hall_booking(

    hall,

    booking_date,

    from_time,

    to_time

):

    if from_time >= to_time:

        return (

            False,

            "Invalid time slot."

        )

    bookings = HallBooking.objects.filter(

        hall=hall,

        booking_date=booking_date,

        status="APPROVED"

    )

    for booking in bookings:

        if is_overlap(

            from_time,

            to_time,

            booking.from_time,

            booking.to_time

        ):

            return (

                False,

                "Hall already booked."

            )

    return (

        True,

        ""

    )


def calculate_equipment_fee(

    equipment,

    from_time,

    to_time

):

    duration = (

        (

            datetime.combine(

                datetime.today(),

                to_time

            )

            -

            datetime.combine(

                datetime.today(),

                from_time

            )

        ).seconds

        /

        3600

    )

    return (

        duration

        *

        equipment.fee_per_hour

    )


def calculate_full_lab_fee(

    lab,

    from_time,

    to_time

):

    equipments = Equipment.objects.filter(

        lab=lab

    )

    total = 0

    for equipment in equipments:

        total += calculate_equipment_fee(

            equipment,

            from_time,

            to_time

        )

    return total


def calculate_lab_fee(

    booking_type,

    lab,

    equipments,

    from_time,

    to_time

):

    if booking_type == "FULL_LAB":

        return calculate_full_lab_fee(

            lab,

            from_time,

            to_time

        )

    total = 0

    for equipment in equipments:

        total += calculate_equipment_fee(

            equipment,

            from_time,

            to_time

        )

    return total

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

        remarks=remarks,

    )