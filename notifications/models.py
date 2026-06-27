from django.db import models
from startups.models import Startup


class Notification(models.Model):

    NOTIFICATION_TYPES = [

        ("LAB", "Lab Booking"),

        ("HALL", "Hall Booking"),

    ]

    startup = models.ForeignKey(
        Startup,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    notification_type = models.CharField(
        max_length=10,
        choices=NOTIFICATION_TYPES,
    )

    booking_id = models.PositiveIntegerField()

    title = models.CharField(
        max_length=200,
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = [
            "-created_at"
        ]

    def __str__(self):

        return self.title