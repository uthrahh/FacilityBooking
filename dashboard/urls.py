from django.urls import path
from bookings.views import (
    update_lab_booking_status,
    update_hall_booking_status,
)
from .views import (
    admin_dashboard,
    startup_dashboard,
    calendar,
    startup_list,
    startup_add,

    lab_list,
    lab_add,

    equipment_list,
    equipment_add,

    hall_list,
    hall_add,

    lab_booking_list,
    hall_booking_list,
)

urlpatterns = [

    # ==========================
    # Dashboards
    # ==========================

    path(
        "dashboard/",
        startup_dashboard,
        name="startup_dashboard",
    ),

    path(
        "admin-dashboard/",
        admin_dashboard,
        name="admin_dashboard",
    ),

    path(
        "calendar/",
        calendar,
        name="calendar",
    ),

    # ==========================
    # Startup Management
    # ==========================

    path(
        "admin/startups/",
        startup_list,
        name="startup_list",
    ),

    path(
        "admin/startups/add/",
        startup_add,
        name="startup_add",
    ),

    # ==========================
    # Lab Management
    # ==========================

    path(
        "admin/labs/",
        lab_list,
        name="lab_list",
    ),

    path(
        "admin/labs/add/",
        lab_add,
        name="lab_add",
    ),

    # ==========================
    # Equipment Management
    # ==========================

    path(
        "admin/equipment/",
        equipment_list,
        name="equipment_list",
    ),

    path(
        "admin/equipment/add/",
        equipment_add,
        name="equipment_add",
    ),

    # ==========================
    # Hall Management
    # ==========================

    path(
        "admin/halls/",
        hall_list,
        name="hall_list",
    ),

    path(
        "admin/halls/add/",
        hall_add,
        name="hall_add",
    ),

    # ==========================
    # Booking Management
    # ==========================

    path(
        "admin/lab-bookings/",
        lab_booking_list,
        name="lab_booking_list",
    ),

    path(
        "admin/hall-bookings/",
        hall_booking_list,
        name="hall_booking_list",
    ),

    path(
        "admin/lab-bookings/status/<int:booking_id>/",
        update_lab_booking_status,
        name="update_lab_booking_status",
    ),

    path(
        "admin/hall-bookings/status/<int:booking_id>/",
        update_hall_booking_status,
        name="update_hall_booking_status",
    ),

]