from django.db import models


class Lab(models.Model):

    lab_id = models.CharField(
        max_length=10,
        unique=True
    )

    name = models.CharField(
        max_length=255
    )

    def __str__(self):
        return self.name


class Equipment(models.Model):

    equipment_id = models.CharField(
        max_length=20,
        unique=True
    )

    name = models.CharField(
        max_length=255
    )

    lab = models.ForeignKey(
        Lab,
        on_delete=models.CASCADE,
        related_name="equipments"
    )

    fee_per_hour = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return self.name