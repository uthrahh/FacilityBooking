from django.contrib import admin
from django.urls import path
from django.urls import include
from django.shortcuts import redirect


def home(request):

    return redirect(
        "startup_login"
    )


urlpatterns = [
    path(
        "",
        include(
            "core.urls"
        )
    ),
    path(
        "",
        home
    ),

    path(
        "",
        include(
            "accounts.urls"
        )
    ),

    path(
        "",
        include(
            "bookings.urls"
        )
    ),

    path(
        "",
        include(
            "dashboard.urls"
        )
    ),

    path(
        "notifications/",
        include(
            "notifications.urls"
        )
    ),

]