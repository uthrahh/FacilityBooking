from django.db import models

from django.core.validators import (
    RegexValidator,
    EmailValidator,
)


startup_id_validator = RegexValidator(
    regex=r"^\d{4}$",
    message="Startup ID must contain exactly 4 digits."
)


phone_validator = RegexValidator(
    regex=r"^[0-9]{10}$",
    message="Phone number must contain exactly 10 digits."
)


class Startup(models.Model):

    startup_id = models.CharField(
        max_length=4,
        unique=True,
        validators=[
            startup_id_validator
        ]
    )

    name = models.CharField(
        max_length=200
    )

    email = models.EmailField(
        unique=True,
        validators=[
            EmailValidator()
        ]
    )

    phone = models.CharField(
        max_length=10,
        blank=True,
        validators=[
            phone_validator
        ]
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

    class Meta:

        ordering = [
            "startup_id"
        ]

    def __str__(self):

        return (
            f"{self.startup_id}"
            " - "
            f"{self.name}"
        )