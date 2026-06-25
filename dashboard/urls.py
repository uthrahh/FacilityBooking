from django.urls import path

from .views import *

urlpatterns = [

    path(
        "dashboard/",
        startup_dashboard,
        name="startup_dashboard"
    ),

    path(
        "admin-dashboard/",
        admin_dashboard,
        name="admin_dashboard"
    ),

    path(
        "calendar/",
        calendar_view,
        name="calendar"
    ),
    path(
        "admin-dashboard/",
        admin_dashboard,
        name="admin_dashboard"
    ),

    path(
        "admin/startups/",
        startup_list,
        name="startup_list"
    ),

    path(
        "admin/startups/add/",
        startup_add,
        name="startup_add"
    ),

    path(
        "admin/labs/",
        lab_list,
        name="lab_list"
    ),

    path(
        "admin/labs/add/",
        lab_add,
        name="lab_add"
    ),

    path(
        "admin/lab-bookings/",
        lab_booking_list,
        name="lab_booking_list"
    ),

    path(
        "admin/lab-bookings/approve/<int:booking_id>/",
        approve_lab_booking,
        name="approve_lab_booking"
    ),
]