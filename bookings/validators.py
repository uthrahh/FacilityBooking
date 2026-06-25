from django.core.exceptions import ValidationError


def validate_hall_capacity(
    seats,
    capacity
):
    if seats > capacity:

        raise ValidationError(
            "Seats cannot exceed hall capacity."
        )