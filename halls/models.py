from django.db import models

from django.core.validators import (
    RegexValidator,
    MinValueValidator,
)

hall_id_validator = RegexValidator(
    regex=r"^H\d{2}$",
    message="Hall ID must be in the format H01."
)


class Hall(models.Model):

    hall_id = models.CharField(
        max_length=3,
        unique=True,
        validators=[
            hall_id_validator
        ]
    )

    name = models.CharField(
        max_length=200
    )

    capacity = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )

    description = models.TextField(
        blank=True
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
            "hall_id"
        ]

    def __str__(self):

        return (
            f"{self.hall_id}"
            " - "
            f"{self.name}"
        )