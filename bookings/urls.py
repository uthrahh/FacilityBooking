from django.urls import path
from .views import (
    create_lab_booking,
    create_hall_booking,
    my_bookings,
    cancel_lab_booking,
    cancel_hall_booking,
    calendar_events,
    available_equipment,
    edit_lab_booking,
    edit_hall_booking
)
from .api import equipment_api
from .api import (
    equipment_api,
    lab_availability_api,
    hall_availability_api
)
from .api import equipment_api

urlpatterns = [

    path(
        "labs/book/",
        create_lab_booking,
        name="lab_booking"
    ),

    path(
        "halls/book/",
        create_hall_booking,
        name="hall_booking"
    ),

    path(
        "my-bookings/",
        my_bookings,
        name="my_bookings"
    ),
    path(
        "lab/cancel/<int:booking_id>/",
        cancel_lab_booking,
        name="cancel_lab_booking"
    ),

    path(
        "hall/cancel/<int:booking_id>/",
        cancel_hall_booking,
        name="cancel_hall_booking"
    ),
    path(
        "calendar/events/",
        calendar_events,
        name="calendar_events"
    ),
    path(
        "equipment/<int:lab_id>/",
        available_equipment,
        name="available_equipment"
    ),
    path(
        "api/equipment/<int:lab_id>/",
        equipment_api,
        name="equipment_api"
    ),
    path(
        "api/equipment/<int:lab_id>/",
        equipment_api,
        name="equipment_api"
    ),

    path(
        "api/lab-availability/<int:lab_id>/",
        lab_availability_api,
        name="lab_availability_api"
    ),

    path(
        "api/hall-availability/<int:hall_id>/",
        hall_availability_api,
        name="hall_availability_api"
    ),
    path(
        "api/equipment/<int:lab_id>/",
        equipment_api,
        name="equipment_api"
    ),
    path(
        "lab/edit/<int:booking_id>/",
        edit_lab_booking,
        name="edit_lab_booking"
    ),

    path(
        "hall/edit/<int:booking_id>/",
        edit_hall_booking,
        name="edit_hall_booking"
    ),
]