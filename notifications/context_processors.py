from .models import Notification


def notification_count(request):

    return {
        "unread_notifications": Notification.objects.filter(
            is_read=False
        ).count()
    }