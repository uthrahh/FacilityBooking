from startups.models import Startup

from .models import Notification


def notification_count(
    request
):

    count = 0

    startup_id = request.session.get(
        "startup_id"
    )

    if startup_id:

        try:

            startup = Startup.objects.get(
                id=startup_id
            )

            count = (
                Notification.objects.filter(
                    startup=startup,
                    is_read=False
                ).count()
            )

        except Startup.DoesNotExist:

            pass

    return {
        "unread_notifications":
        count
    }