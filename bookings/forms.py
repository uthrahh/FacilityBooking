from django import forms

from labs.models import Lab
from labs.models import Equipment

from halls.models import Hall
from .models import HallBooking


BOOKING_TYPE_CHOICES = [
    ("FULL_LAB", "Book Full Lab"),
    ("EQUIPMENT", "Book Equipment"),
]


class LabBookingForm(forms.Form):

    lab = forms.ModelChoiceField(
        queryset=Lab.objects.all()
    )

    booking_type = forms.ChoiceField(
        choices=BOOKING_TYPE_CHOICES
    )

    booking_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"}
        )
    )

    from_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={"type": "time"}
        )
    )

    to_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={"type": "time"}
        )
    )

    equipments = forms.ModelMultipleChoiceField(
        queryset=Equipment.objects.all(),
        required=False
    )


class HallBookingForm(forms.Form):

    hall = forms.ModelChoiceField(
        queryset=Hall.objects.all()
    )

    booking_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"}
        )
    )

    from_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={"type": "time"}
        )
    )

    to_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={"type": "time"}
        )
    )

    ac = forms.BooleanField(
        required=False
    )

    projector = forms.BooleanField(
        required=False
    )

    seats = forms.IntegerField(
        min_value=0
    )

    mic_qty = forms.IntegerField(
        min_value=0,
        required=False
    )

    water_bottle_qty = forms.IntegerField(
        min_value=0,
        required=False
    )

    class Meta:

            model = HallBooking

            fields = [
                "hall",
                "booking_date",
                "from_time",
                "to_time",
                "ac",
                "projector",
                "seats",
                "mic_qty",
                "water_bottle_qty",
            ]
    
    def clean(self):

        cleaned_data = super().clean()

        hall = cleaned_data.get("hall")
        seats = cleaned_data.get("seats")

        if hall and seats:

            if seats > hall.capacity:

                raise forms.ValidationError(
                    "Seats exceed hall capacity."
                )

        return cleaned_data