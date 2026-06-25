from django.db import models


class Hall(models.Model):

    hall_id = models.CharField(
        max_length=10,
        unique=True
    )

    name = models.CharField(
        max_length=255
    )

    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name