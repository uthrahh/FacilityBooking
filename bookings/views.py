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
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
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
from datetime import datetime

from decimal import Decimal
from notifications.models import (
    Notification
)

from .models import (
    LabBooking,
    HallBooking,
    LabBookingEquipment,
    BookingHistory
)
from notifications.services import (
    create_lab_booking_notification,
    create_hall_booking_notification,
    booking_status_notification,
)

from accounts.decorators import (
    startup_login_required,
    admin_login_required
)
from dashboard.forms import HallForm

from .models import BookingHistory


def create_history(
    booking_type,
    booking_id,
    old_status,
    new_status,
    remarks=""
):

    BookingHistory.objects.create(

        booking_type=booking_type,

        booking_id=booking_id,

        old_status=old_status,

        new_status=new_status,

        remarks=remarks,

    )
    
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

from datetime import datetime
from decimal import Decimal

@startup_login_required
def create_lab_booking(request):

    if not request.session.get(
        "startup_id"
    ):
        return redirect(
            "startup_login"
        )

    startup = Startup.objects.get(
        id=request.session["startup_id"]
    )

    if request.method == "POST":

        form = LabBookingForm(
            request.POST
        )

        if form.is_valid():

            lab = form.cleaned_data["lab"]

            booking_date = (
                form.cleaned_data[
                    "booking_date"
                ]
            )

            equipment_ids = (
                request.POST.getlist(
                    "equipment"
                )
            )
            booking_type = request.POST.get(
                "booking_type"
            )
            from_times = (
                request.POST.getlist(
                    "from_time"
                )
            )

            to_times = (
                request.POST.getlist(
                    "to_time"
                )
            )

            booking = LabBooking.objects.create(
                startup=startup,
                lab=lab,
                booking_date=booking_date,
                status="NEW"
            )

            total_fee = Decimal("0")

            first_from = None
            first_to = None
            if booking_type == "FULL_LAB":

                booking.is_full_lab = True

                booking.from_time = form.cleaned_data[
                    "from_time"
                ]

                booking.to_time = form.cleaned_data[
                    "to_time"
                ]

                booking.save()

                create_lab_booking_notification(
                    booking
                )

                messages.success(
                    request,
                    "Full Lab Booking Submitted"
                )

                return redirect(
                    "my_bookings"
                )
            
            for i in range(
                len(equipment_ids)
            ):

                if not equipment_ids[i]:
                    continue

                equipment = (
                    Equipment.objects.get(
                        id=equipment_ids[i]
                    )
                )

                start = datetime.strptime(
                    from_times[i],
                    "%H:%M"
                )

                end = datetime.strptime(
                    to_times[i],
                    "%H:%M"
                )

                duration = Decimal(
                    str(
                        (
                            end - start
                        ).seconds / 3600
                    )
                )

                fee = (
                    equipment.fee_per_hour
                    * duration
                )

                approved = (
                    LabBookingEquipment.objects.filter(
                        equipment=equipment,
                        booking__booking_date=booking_date,
                        booking__status="APPROVED"
                    )
                )

                conflict = False

                for existing in approved:

                    if (
                        from_times[i]
                        <
                        existing.to_time.strftime("%H:%M")
                        and
                        to_times[i]
                        >
                        existing.from_time.strftime("%H:%M")
                    ):
                        conflict = True
                        break

                if conflict:

                    booking.delete()

                    messages.error(
                        request,
                        f"{equipment.name} already booked for selected time"
                    )

                    return render(
                        request,
                        "bookings/lab_booking.html",
                        {
                            "form": form
                        }
                    )

                if first_from is None:

                    first_from = datetime.strptime(
                        from_times[i],
                        "%H:%M"
                    ).time()

                    first_to = datetime.strptime(
                        to_times[i],
                        "%H:%M"
                    ).time()

                LabBookingEquipment.objects.create(
                    booking=booking,
                    equipment=equipment,
                    from_time=first_from if i == 0 else datetime.strptime(
                        from_times[i],
                        "%H:%M"
                    ).time(),
                    to_time=first_to if i == 0 else datetime.strptime(
                        to_times[i],
                        "%H:%M"
                    ).time(),
                    hours=duration,
                    equipment_fee=fee
                )

                total_fee += fee

            booking.from_time = first_from
            booking.to_time = first_to
            booking.estimated_fee = total_fee

            booking.save()
            create_lab_booking_notification(
                booking
            )
            messages.success(
                request,
                "Booking Created Successfully"
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
            booking = HallBooking.objects.create(
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
            create_hall_booking_notification(
                booking
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

    create_history(
        "LAB",
        booking.id,
        old_status,
        "CANCELLED"
    )

    booking.status = "CANCELLED"

    booking.save()

    BookingHistory.objects.create(

        booking_type="LAB",

        booking_id=booking.id,

        old_status="NEW",

        new_status="CANCELLED",

    )

    messages.info(

        request,

        "Previous booking cancelled. Submit the updated booking."

    )

    return redirect(

        "lab_booking"

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

    BookingHistory.objects.create(

        booking_type="HALL",

        booking_id=booking.id,

        old_status="NEW",

        new_status="CANCELLED",

    )

    messages.info(

        request,

        "Previous booking cancelled. Submit the updated booking."

    )

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
                "title": f"{booking.lab.lab_id} - {booking.startup.startup_id}",
                "start": f"{booking.booking_date}T{booking.from_time}",
                "end": f"{booking.booking_date}T{booking.to_time}",
                "id": booking.id,
                "url": f"/admin/lab-bookings/#booking-{booking.id}",
                "lab": "#D6EAF8",
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
                "title": f"{booking.hall.hall_id} - {booking.startup.startup_id}",
                "start": f"{booking.booking_date}T{booking.from_time}",
                "end": f"{booking.booking_date}T{booking.to_time}",
                "id": booking.id,
                "url": f"/admin/hall-bookings/#booking-{booking.id}",
                "hall": "#FDEBD0",
            }
        )

    return JsonResponse(
        events,
        safe=False
    )

@admin_login_required
@require_POST
def update_lab_booking_status(
    request,
    booking_id
):

    booking = get_object_or_404(
        LabBooking,
        id=booking_id
    )

    old_status = booking.status

    new_status = request.POST.get(
        "status"
    )

    booking.status = new_status

    booking.save()

    BookingHistory.objects.create(
        booking_type="LAB",
        booking_id=booking.id,
        old_status=old_status,
        new_status=new_status,
        remarks=""
    )

    booking_status_notification(

        booking,

        "LAB"

    )

    return redirect(
        "lab_booking_list"
    )

@admin_login_required
@require_POST
def update_hall_booking_status(
    request,
    booking_id
):

    booking = get_object_or_404(
        HallBooking,
        id=booking_id
    )

    old_status = booking.status

    new_status = request.POST.get(
        "status"
    )

    booking.status = new_status

    booking.save()

    BookingHistory.objects.create(
        booking_type="HALL",
        booking_id=booking.id,
        old_status=old_status,
        new_status=new_status,
        remarks=""
    )

    booking_status_notification(

        booking,

        "HALL"

    )

    return redirect(
        "hall_booking_list"
    )

@admin_login_required
def hall_list(request):

    halls = Hall.objects.all()

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

@startup_login_required
def lab_availability(
    request,
    lab_id
):

    date = request.GET.get(
        "date"
    )

    bookings = (

        LabBooking.objects

        .filter(

            lab_id=lab_id,

            booking_date=date,

            status="APPROVED"

        )

    )

    data = []

    for booking in bookings:

        data.append(

            {

                "startup":

                booking.startup.startup_id,

                "from":

                booking.from_time.strftime(

                    "%H:%M"

                ),

                "to":

                booking.to_time.strftime(

                    "%H:%M"

                ),

            }

        )

    return JsonResponse(

        data,

        safe=False

    )

@startup_login_required
def hall_availability(
    request,
    hall_id
):

    date = request.GET.get(
        "date"
    )

    bookings = (

        HallBooking.objects

        .filter(

            hall_id=hall_id,

            booking_date=date,

            status="APPROVED"

        )

    )

    data = []

    for booking in bookings:

        data.append(

            {

                "startup":

                booking.startup.startup_id,

                "from":

                booking.from_time.strftime(

                    "%H:%M"

                ),

                "to":

                booking.to_time.strftime(

                    "%H:%M"

                ),

            }

        )

    return JsonResponse(

        data,

        safe=False

    )