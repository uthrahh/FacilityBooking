from django.shortcuts import render
from django.shortcuts import redirect

from accounts.decorators import admin_login_required

from .models import Notification

from bookings.models import (
    LabBooking,
    HallBooking,
)


@admin_login_required
def notification_list(request):

    notifications = (
        Notification.objects
        .filter(is_read=False)
        .order_by("-created_at")
    )

    lab_notifications = (
        LabBooking.objects
        .select_related(
            "startup",
            "lab"
        )
        .filter(
            status="NEW"
        )
        .order_by(
            "-booking_timestamp"
        )
    )

    hall_notifications = (
        HallBooking.objects
        .select_related(
            "startup",
            "hall"
        )
        .filter(
            status="NEW"
        )
        .order_by(
            "-booking_timestamp"
        )
    )

    notification_count = (
        lab_notifications.count()
        +
        hall_notifications.count()
    )

    return render(
        request,
        "dashboard/notification_list.html",
        {
            "notifications": notifications,
            "lab_notifications": lab_notifications,
            "hall_notifications": hall_notifications,
            "notification_count": notification_count,
        },
    )


@admin_login_required
def mark_notification_read(
    request,
    notification_id
):

    try:

        notification = Notification.objects.get(
            id=notification_id
        )

        notification.is_read = True

        notification.save()

    except Notification.DoesNotExist:

        pass

    return redirect(
        "notification_list"
    )


@admin_login_required
def mark_all_notifications_read(
    request
):

    Notification.objects.filter(
        is_read=False
    ).update(
        is_read=True
    )

    return redirect(
        "notification_list"
    )