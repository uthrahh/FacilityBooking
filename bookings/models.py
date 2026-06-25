from django.db import models

BOOKING_STATUS = [
    ("NEW", "New Booking"),
    ("APPROVED", "Approved"),
    ("REJECTED", "Rejected"),
    ("CANCELLED", "Cancelled"),
]
class LabBooking(models.Model):

    startup = models.ForeignKey(
        "startups.Startup",
        on_delete=models.CASCADE
    )

    lab = models.ForeignKey(
        "labs.Lab",
        on_delete=models.CASCADE
    )

    booking_date = models.DateField()

    from_time = models.TimeField(
        null=True,
        blank=True
    )

    to_time = models.TimeField(
        null=True,
        blank=True
    )

    estimated_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    is_full_lab = models.BooleanField(
        default=False
    )

    status = models.CharField(
        max_length=20,
        choices=BOOKING_STATUS,
        default="NEW"
    )

    booking_timestamp = models.DateTimeField(
        auto_now_add=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    admin_remarks = models.TextField(
        blank=True,
        null=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):
        return f"{self.startup} - {self.lab} - {self.booking_date}"


class LabBookingEquipment(models.Model):

    booking = models.ForeignKey(
        LabBooking,
        on_delete=models.CASCADE,
        related_name="equipments"
    )

    equipment = models.ForeignKey(
        "labs.Equipment",
        on_delete=models.CASCADE
    )

    from_time = models.TimeField()

    to_time = models.TimeField()

    hours = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    equipment_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.booking.id} - {self.equipment.name}"

class HallBooking(models.Model):

    startup = models.ForeignKey(
        "startups.Startup",
        on_delete=models.CASCADE
    )

    hall = models.ForeignKey(
        "halls.Hall",
        on_delete=models.CASCADE
    )
    booking_date = models.DateField()

    from_time = models.TimeField()

    to_time = models.TimeField()
    ac = models.BooleanField(
        default=False
    )

    projector = models.BooleanField(
        default=False
    )

    seats = models.PositiveIntegerField(
        default=0
    )

    mic_qty = models.PositiveIntegerField(
        default=0
    )

    water_bottle_qty = models.PositiveIntegerField(
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=BOOKING_STATUS,
        default="NEW"
    )

    booking_timestamp = models.DateTimeField(
        auto_now_add=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    admin_remarks = models.TextField(
        blank=True,
        null=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.startup} - {self.hall} - {self.booking_date}"

class BookingHistory(models.Model):

    booking_type = models.CharField(
        max_length=20
    )

    booking_id = models.PositiveIntegerField()

    old_status = models.CharField(
        max_length=20
    )

    new_status = models.CharField(
        max_length=20
    )

    remarks = models.TextField(
        blank=True
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.booking_type} - {self.booking_id}"