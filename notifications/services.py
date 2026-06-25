from .models import Notification


def create_notification(
    startup,
    title,
    message
):

    Notification.objects.create(
        startup=startup,
        title=title,
        message=message
    )