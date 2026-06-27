from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


def home(request):
    if request.user.is_authenticated:
        return redirect("admin_dashboard")

    if request.session.get("startup_id"):
        return redirect("startup_dashboard")

    return redirect("startup_login")


urlpatterns = [

    path(
        "",
        home,
        name="home",
    ),

    # Keep Django admin only if you still want it available
    path(
        "django-admin/",
        admin.site.urls,
    ),

    path(
        "",
        include("accounts.urls"),
    ),

    path(
        "",
        include("bookings.urls"),
    ),

    path(
        "",
        include("dashboard.urls"),
    ),

    path(
        "",
        include("notifications.urls"),
    ),

]