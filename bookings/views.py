from decimal import Decimal
from django.contrib import messages
from django.http import JsonResponse
from startups.models import Startup
from labs.models import Equipment
from halls.models import Hall
from accounts.decorators import (
    startup_login_required
)
from .utils import is_overlap
from .forms import (
    LabBookingForm,
    HallBookingForm
)

from django.shortcuts import (
    render,
    redirect
)
from django.http import JsonResponse

from datetime import datetime
from datetime import timedelta

from labs.models import Equipment
from .models import (
    LabBooking,
    HallBooking,
    LabBookingEquipment
)
from .services import (
    validate_lab_booking,
    validate_hall_booking,
    create_history
)

from django.http import JsonResponse
from labs.models import Equipment
from .models import LabBookingEquipment


@startup_login_required
def available_equipment(
    request,
    lab_id
):

    date = request.GET.get(
        "date"
    )

    equipments = (
        Equipment.objects.filter(
            lab_id=lab_id
        )
    )

    response = []

    for equipment in equipments:

        occupied = []

        bookings = (
            LabBookingEquipment.objects.filter(
                equipment=equipment,
                booking__booking_date=date,
                booking__status="APPROVED"
            )
        )

        for booking in bookings:

            occupied.append(
                {
                    "from":
                    booking.from_time.strftime(
                        "%H:%M"
                    ),

                    "to":
                    booking.to_time.strftime(
                        "%H:%M"
                    )
                }
            )

        response.append(
            {
                "id":
                equipment.id,

                "name":
                equipment.name,

                "rate":
                float(
                    equipment.fee_per_hour
                ),

                "occupied":
                occupied
            }
        )

    return JsonResponse(
        response,
        safe=False
    )

@startup_login_required
def create_lab_booking(request):

    if not request.session.get("startup_id"):
        return redirect("startup_login")

    startup = Startup.objects.get(
        id=request.session["startup_id"]
    )

    if request.method == "POST":

        form = LabBookingForm(request.POST)

        if form.is_valid():

            booking_type = form.cleaned_data["booking_type"]

            lab = form.cleaned_data["lab"]

            booking_date = form.cleaned_data["booking_date"]

            from_time = form.cleaned_data["from_time"]

            to_time = form.cleaned_data["to_time"]

            equipments = form.cleaned_data["equipments"]
            valid, message = validate_lab_booking(
                lab,
                equipments,
                booking_date,
                from_time,
                to_time,
                booking_type == "FULL_LAB"
            )

            if not valid:

                messages.error(
                    request,
                    message
                )

                return render(
                    request,
                    "bookings/lab_booking.html",
                    {
                        "form": form
                    }
                )
            booking = LabBooking.objects.create(
                startup=startup,
                lab=lab,
                booking_date=booking_date,
                from_time=from_time,
                to_time=to_time,
                is_full_lab=(
                    booking_type == "FULL_LAB"
                )
            )

            total_fee = Decimal("0")

            if booking_type == "EQUIPMENT":

                for equipment in equipments:

                    duration = (
                        (
                            to_time.hour * 60
                            + to_time.minute
                        )
                        -
                        (
                            from_time.hour * 60
                            + from_time.minute
                        )
                    ) / 60

                    fee = (
                        equipment.fee_per_hour
                        * Decimal(str(duration))
                    )

                    LabBookingEquipment.objects.create(
                        booking=booking,
                        equipment=equipment,
                        from_time=from_time,
                        to_time=to_time,
                        hours=duration,
                        equipment_fee=fee
                    )

                    total_fee += fee

            else:

                equipments = Equipment.objects.filter(
                    lab=lab
                )

                duration = (
                    (
                        to_time.hour * 60
                        + to_time.minute
                    )
                    -
                    (
                        from_time.hour * 60
                        + from_time.minute
                    )
                ) / 60

                for equipment in equipments:

                    total_fee += (
                        equipment.fee_per_hour
                        * Decimal(str(duration))
                    )

            booking.estimated_fee = total_fee
            existing = LabBooking.objects.filter(
                lab=lab,
                booking_date=booking_date,
                status="APPROVED"
            )

            for item in existing:

                if (
                    item.from_time
                    and
                    item.to_time
                    and
                    is_overlap(
                        from_time,
                        to_time,
                        item.from_time,
                        item.to_time
                    )
                ):
                    messages.error(
                        request,
                        "Selected slot unavailable"
                    )

                    booking.delete()

                    return render(
                        request,
                        "bookings/lab_booking.html",
                        {
                            "form": form
                        }
                    )

            booking.estimated_fee = total_fee
            booking.save()

            messages.success(
                request,
                "Booking Created"
            )

            return redirect(
                "my_bookings"
            )

    else:

        form = LabBookingForm()

    return render(
        request,
        "bookings/lab_booking.html",
        {
            "form": form
        }
    )

@startup_login_required
def create_hall_booking(request):

    if not request.session.get("startup_id"):
        return redirect("startup_login")

    startup = Startup.objects.get(
        id=request.session["startup_id"]
    )

    if request.method == "POST":

        form = HallBookingForm(request.POST)

        if form.is_valid():
            valid, message = validate_hall_booking(
                form.cleaned_data["hall"],
                form.cleaned_data["booking_date"],
                form.cleaned_data["from_time"],
                form.cleaned_data["to_time"]
            )

            if not valid:

                messages.error(
                    request,
                    message
                )

                return render(
                    request,
                    "bookings/hall_booking.html",
                    {
                        "form": form
                    }
                )
            HallBooking.objects.create(
                startup=startup,
                hall=form.cleaned_data["hall"],
                booking_date=form.cleaned_data["booking_date"],
                from_time=form.cleaned_data["from_time"],
                to_time=form.cleaned_data["to_time"],
                ac=form.cleaned_data["ac"],
                projector=form.cleaned_data["projector"],
                seats=form.cleaned_data["seats"],
                mic_qty=form.cleaned_data["mic_qty"] or 0,
                water_bottle_qty=form.cleaned_data["water_bottle_qty"] or 0
            )

            messages.success(
                request,
                "Hall Booking Created"
            )

            return redirect(
                "my_bookings"
            )

    else:

        form = HallBookingForm()

    return render(
        request,
        "bookings/hall_booking.html",
        {
            "form": form
        }
    )

@startup_login_required
def my_bookings(request):

    if not request.session.get("startup_id"):
        return redirect("startup_login")

    startup = Startup.objects.get(
        id=request.session["startup_id"]
    )

    lab_bookings = LabBooking.objects.filter(
        startup=startup
    ).order_by("-booking_timestamp")

    hall_bookings = HallBooking.objects.filter(
        startup=startup
    ).order_by("-booking_timestamp")

    return render(
        request,
        "bookings/my_bookings.html",
        {
            "lab_bookings": lab_bookings,
            "hall_bookings": hall_bookings
        }
    )

@startup_login_required
def cancel_lab_booking(
    request,
    booking_id
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

    booking = LabBooking.objects.get(
        id=booking_id,
        startup=startup
    )

    old_status = booking.status

    booking.status = "CANCELLED"

    booking.save()

    create_history(
        "LAB",
        booking.id,
        old_status,
        "CANCELLED"
    )

    return redirect(
        "my_bookings"
    )

@startup_login_required
def cancel_hall_booking(
    request,
    booking_id
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

    booking = HallBooking.objects.get(
        id=booking_id,
        startup=startup
    )

    old_status = booking.status

    booking.status = "CANCELLED"

    booking.save()

    create_history(
        "HALL",
        booking.id,
        old_status,
        "CANCELLED"
    )

    return redirect(
        "my_bookings"
    )

@startup_login_required
def edit_lab_booking(
    request,
    booking_id
):

    booking = LabBooking.objects.get(
        id=booking_id
    )

    booking.status = "CANCELLED"

    booking.save()

    return redirect(
        "lab_booking"
    )

@startup_login_required
def edit_hall_booking(
    request,
    booking_id
):

    booking = HallBooking.objects.get(
        id=booking_id
    )

    booking.status = "CANCELLED"

    booking.save()

    return redirect(
        "hall_booking"
    )

from django.http import JsonResponse


@startup_login_required
def calendar_events(request):

    events = []

    lab_bookings = LabBooking.objects.filter(
        status="APPROVED"
    )

    hall_bookings = HallBooking.objects.filter(
        status="APPROVED"
    )

    for booking in lab_bookings:

        if (
            not booking.from_time
            or
            not booking.to_time
        ):
            continue

        events.append(
            {
                "title": booking.lab.name,
                "start": f"{booking.booking_date}T{booking.from_time}",
                "end": f"{booking.booking_date}T{booking.to_time}",
                "color": "#3498db",
            }
        )

    for booking in hall_bookings:

        if (
            not booking.from_time
            or
            not booking.to_time
        ):
            continue

        events.append(
            {
                "title": booking.hall.name,
                "start": f"{booking.booking_date}T{booking.from_time}",
                "end": f"{booking.booking_date}T{booking.to_time}",
                "color": "#2ecc71",
            }
        )

    return JsonResponse(
        events,
        safe=False
    )