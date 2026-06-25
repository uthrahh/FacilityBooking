from django.db import models


class Startup(models.Model):

    startup_id = models.CharField(
        max_length=4,
        unique=True
    )

    name = models.CharField(
        max_length=255
    )

    founder_name = models.CharField(
        max_length=255
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=20
    )

    incubation_status = models.CharField(
        max_length=100
    )

    password_hash = models.CharField(
        max_length=255
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.startup_id} - {self.name}"