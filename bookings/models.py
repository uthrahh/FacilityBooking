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

    updated_at = models.DateTimeField(
        auto_now=True
    )

    admin_remarks = models.TextField(
        blank=True,
        null=True
    )

    class Meta:

        ordering = [
            "-booking_timestamp"
        ]

    @property
    def equipment_list(self):

        return ", ".join(
            [
                item.equipment.equipment_id +
                " - " +
                item.equipment.name
                for item in self.equipments.select_related(
                    "equipment"
                )
            ]
        )

    def __str__(self):

        return (
            f"{self.startup.startup_id}"
            " - "
            f"{self.lab.lab_id}"
            " - "
            f"{self.booking_date}"
        )


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

    class Meta:

        ordering = [
            "equipment__equipment_id"
        ]

    def __str__(self):

        return (
            f"{self.booking.id}"
            " - "
            f"{self.equipment.name}"
        )


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

    estimated_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
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

    updated_at = models.DateTimeField(
        auto_now=True
    )

    admin_remarks = models.TextField(
        blank=True,
        null=True
    )

    class Meta:

        ordering = [
            "-booking_timestamp"
        ]

    @property
    def utilities(self):

        items = []

        if self.ac:
            items.append("AC")

        if self.projector:
            items.append("Projector")

        if self.seats:
            items.append(
                f"Seats : {self.seats}"
            )

        if self.mic_qty:
            items.append(
                f"Mic : {self.mic_qty}"
            )

        if self.water_bottle_qty:
            items.append(
                f"Water : {self.water_bottle_qty}"
            )

        return ", ".join(items)

    def __str__(self):

        return (
            f"{self.startup.startup_id}"
            " - "
            f"{self.hall.hall_id}"
            " - "
            f"{self.booking_date}"
        )


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

    class Meta:

        ordering = [
            "-timestamp"
        ]

    def __str__(self):

        return (
            f"{self.booking_type}"
            " - "
            f"{self.booking_id}"
            " - "
            f"{self.new_status}"
        )