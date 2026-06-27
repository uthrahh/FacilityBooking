from django.db import models

from django.core.validators import (
    RegexValidator,
    MinValueValidator,
)


lab_id_validator = RegexValidator(
    regex=r"^L\d{2}$",
    message="Lab ID must be in the format L01."
)

equipment_id_validator = RegexValidator(
    regex=r"^L\d{2}E\d{2}$",
    message="Equipment ID must be in the format L01E01."
)


class Lab(models.Model):

    lab_id = models.CharField(
        max_length=3,
        unique=True,
        validators=[
            lab_id_validator
        ]
    )

    name = models.CharField(
        max_length=200
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
            "lab_id"
        ]

    def __str__(self):

        return (
            f"{self.lab_id}"
            " - "
            f"{self.name}"
        )


class Equipment(models.Model):

    equipment_id = models.CharField(
        max_length=6,
        unique=True,
        validators=[
            equipment_id_validator
        ]
    )

    lab = models.ForeignKey(
        Lab,
        on_delete=models.CASCADE,
        related_name="equipments"
    )

    name = models.CharField(
        max_length=200
    )

    fee_per_hour = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0)
        ]
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
            "lab",
            "equipment_id"
        ]

    def __str__(self):

        return (
            f"{self.equipment_id}"
            " - "
            f"{self.name}"
        )