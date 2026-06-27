from .models import Notification

from bookings.models import (
    LabBooking,
    HallBooking,
)


def create_lab_booking_notification(booking):

    Notification.objects.create(

        notification_type="LAB",

        booking_id=booking.id,

        title=f"New Lab Booking - {booking.lab.lab_id}",

        message=(
            f"{booking.startup.startup_id} "
            f"requested "
            f"{booking.lab.name} "
            f"on "
            f"{booking.booking_date} "
            f"from "
            f"{booking.from_time} "
            f"to "
            f"{booking.to_time}."
        )

    )


def create_hall_booking_notification(booking):

    Notification.objects.create(

        notification_type="HALL",

        booking_id=booking.id,

        title=f"New Hall Booking - {booking.hall.hall_id}",

        message=(
            f"{booking.startup.startup_id} "
            f"requested "
            f"{booking.hall.name} "
            f"on "
            f"{booking.booking_date} "
            f"from "
            f"{booking.from_time} "
            f"to "
            f"{booking.to_time}."
        )

    )


def booking_status_notification(booking, booking_type):

    if booking_type == "LAB":

        title = f"Lab Booking {booking.status.title()}"

        message = (
            f"Your booking for "
            f"{booking.lab.name} "
            f"on "
            f"{booking.booking_date} "
            f"has been "
            f"{booking.status.title()}."
        )

    else:

        title = f"Hall Booking {booking.status.title()}"

        message = (
            f"Your booking for "
            f"{booking.hall.name} "
            f"on "
            f"{booking.booking_date} "
            f"has been "
            f"{booking.status.title()}."
        )

    Notification.objects.create(

        notification_type=booking_type,

        booking_id=booking.id,

        title=title,

        message=message,

    )


def unread_notification_count():

    return Notification.objects.filter(

        is_read=False

    ).count()


def latest_notifications(limit=10):

    return (

        Notification.objects

        .order_by("-created_at")[:limit]

    )


def mark_notification_read(notification_id):

    Notification.objects.filter(

        id=notification_id

    ).update(

        is_read=True

    )


def mark_all_notifications_read():

    Notification.objects.filter(

        is_read=False

    ).update(

        is_read=True

    )


def delete_booking_notifications(booking_id, booking_type):

    Notification.objects.filter(

        booking_id=booking_id,

        notification_type=booking_type,

    ).delete()


def sync_notifications():

    """
    Creates notifications for any NEW booking
    that does not already have one.
    Safe to call repeatedly.
    """

    for booking in LabBooking.objects.filter(status="NEW"):

        exists = Notification.objects.filter(

            booking_id=booking.id,

            notification_type="LAB",

        ).exists()

        if not exists:

            create_lab_booking_notification(

                booking

            )

    for booking in HallBooking.objects.filter(status="NEW"):

        exists = Notification.objects.filter(

            booking_id=booking.id,

            notification_type="HALL",

        ).exists()

        if not exists:

            create_hall_booking_notification(

                booking

            )