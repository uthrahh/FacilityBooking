from django.shortcuts import render
from django.shortcuts import redirect
from bookings.models import (
    LabBooking,
    HallBooking,
)
from accounts.decorators import (
    startup_login_required
)
from startups.models import Startup
from labs.models import Lab
from labs.models import Equipment
from halls.models import Hall
from .forms import (
    StartupForm,
    LabForm,
    EquipmentForm,
    HallForm
)

from accounts.decorators import (
    admin_login_required
)

from notifications.models import Notification

@admin_login_required
def admin_dashboard(
    request
):

    return render(
        request,
        "dashboard/admin_dashboard.html",
        {
            "startup_count":
            Startup.objects.count(),

            "lab_count":
            Lab.objects.count(),

            "equipment_count":
            Equipment.objects.count(),

            "hall_count":
            Hall.objects.count(),

            "pending_lab":
            LabBooking.objects.filter(
                status="NEW"
            ).count(),

            "pending_hall":
            HallBooking.objects.filter(
                status="NEW"
            ).count(),

            "notification_count":
            Notification.objects.filter(
                is_read=False
            ).count(),
        }
    )

@startup_login_required
def startup_dashboard(
    request
):

    if not request.session.get(
        "startup_id"
    ):
        return redirect(
            "startup_login"
        )

    startup = Startup.objects.get(
        id=request.session["startup_id"]
    )

    lab_count = (
        LabBooking.objects.filter(
            startup=startup
        ).count()
    )

    hall_count = (
        HallBooking.objects.filter(
            startup=startup
        ).count()
    )

    pending_count = (
        LabBooking.objects.filter(
            startup=startup,
            status="NEW"
        ).count()
        +
        HallBooking.objects.filter(
            startup=startup,
            status="NEW"
        ).count()
    )

    approved_count = (
        LabBooking.objects.filter(
            startup=startup,
            status="APPROVED"
        ).count()
        +
        HallBooking.objects.filter(
            startup=startup,
            status="APPROVED"
        ).count()
    )

    return render(
        request,
        "dashboard/dashboard.html",
        {
            "startup": startup,
            "lab_count": lab_count,
            "hall_count": hall_count,
            "pending_count": pending_count,
            "approved_count": approved_count
        }
    )

@admin_login_required
def calendar(request):

    return render(
        request,
        "dashboard/calendar.html",
    )

@admin_login_required
def startup_list(request):

    startups = Startup.objects.order_by(
        "startup_id"
    )

    return render(
        request,
        "dashboard/startup_list.html",
        {
            "startups": startups
        }
    )


@admin_login_required
def startup_add(request):

    form = StartupForm(
        request.POST or None
    )

    if form.is_valid():

        form.save()

        return redirect(
            "startup_list"
        )

    return render(
        request,
        "dashboard/startup_form.html",
        {
            "form": form
        }
    )

@admin_login_required
def lab_list(request):

    labs = Lab.objects.order_by(
        "lab_id"
    )

    return render(
        request,
        "dashboard/lab_list.html",
        {
            "labs": labs
        }
    )


@admin_login_required
def lab_add(request):

    form = LabForm(
        request.POST or None
    )

    if form.is_valid():

        form.save()

        return redirect(
            "lab_list"
        )

    return render(
        request,
        "dashboard/lab_form.html",
        {
            "form": form
        }
    )

@admin_login_required
def lab_booking_list(request):

    bookings = (

        LabBooking.objects

        .select_related(

            "startup",

            "lab"

        )

        .prefetch_related(

            "equipments",

            "equipments__equipment"

        )

        .order_by(

            "-booking_timestamp"

        )

    )

    return render(
        request,
        "dashboard/lab_booking_list.html",
        {
            "bookings": bookings
        }
    )

@admin_login_required
def equipment_list(
    request
):

    equipments = (

        Equipment.objects

        .select_related(
            "lab"
        )

        .order_by(
            "equipment_id"
        )

    )

    return render(
        request,
        "dashboard/equipment_list.html",
        {
            "equipments":
            equipments
        }
    )


@admin_login_required
def equipment_add(request):

    form = EquipmentForm(
        request.POST or None
    )

    if form.is_valid():

        form.save()

        return redirect(
            "equipment_list"
        )

    return render(
        request,
        "dashboard/equipment_form.html",
        {
            "form": form
        }
    )


@admin_login_required
def hall_list(request):

    halls = Hall.objects.order_by(
        "hall_id"
    )

    return render(
        request,
        "dashboard/hall_list.html",
        {
            "halls": halls
        }
    )


@admin_login_required
def hall_add(request):

    form = HallForm(
        request.POST or None
    )

    if form.is_valid():

        form.save()

        return redirect(
            "hall_list"
        )

    return render(
        request,
        "dashboard/hall_form.html",
        {
            "form": form
        }
    )


@admin_login_required
def hall_booking_list(request):

    bookings = (

        HallBooking.objects

        .select_related(

            "startup",

            "hall"

        )

        .order_by(

            "-booking_timestamp"

        )

    )

    return render(
        request,
        "dashboard/hall_booking_list.html",
        {
            "bookings": bookings
        }
    )


@admin_login_required
def notification_list(request):

    notifications = (
        Notification.objects
        .order_by("-created_at")
    )

    return render(
        request,
        "dashboard/notification_list.html",
        {
            "notifications": notifications
        }
    )