from django.shortcuts import (
    render,
    redirect
)

from startups.models import Startup

from .models import Notification
from accounts.decorators import (
    startup_login_required
)

@startup_login_required
def notification_list(
    request
):

    if not request.session.get(
        "startup_id"
    ):
        return redirect(
            "startup_login"
        )

    startup = Startup.objects.get(
        id=request.session[
            "startup_id"
        ]
    )

    notifications = (
        Notification.objects.filter(
            startup=startup
        )
        .order_by(
            "-created_at"
        )
    )

    notifications.update(
        is_read=True
    )

    return render(
        request,
        "notifications/list.html",
        {
            "notifications":
            notifications
        }
    )