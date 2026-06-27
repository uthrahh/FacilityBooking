from django import forms

from labs.models import (
    Lab,
    Equipment,
)

from halls.models import Hall

from .models import HallBooking


BOOKING_TYPE_CHOICES = [

    ("FULL_LAB", "Book Full Lab"),

    ("EQUIPMENT", "Book Equipment"),

]


class LabBookingForm(forms.Form):

    lab = forms.ModelChoiceField(

        queryset=Lab.objects.all(),

        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )

    )

    booking_type = forms.ChoiceField(

        choices=BOOKING_TYPE_CHOICES,

        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )

    )

    booking_date = forms.DateField(

        widget=forms.DateInput(

            attrs={
                "type": "date",
                "class": "form-control"
            }

        )

    )

    from_time = forms.TimeField(

        widget=forms.TimeInput(

            attrs={
                "type": "time",
                "class": "form-control"
            }

        )

    )

    to_time = forms.TimeField(

        widget=forms.TimeInput(

            attrs={
                "type": "time",
                "class": "form-control"
            }

        )

    )

    equipments = forms.ModelMultipleChoiceField(

        queryset=Equipment.objects.none(),

        required=False,

        widget=forms.SelectMultiple(

            attrs={
                "class": "form-select"
            }

        )

    )

    def __init__(

        self,
        *args,
        **kwargs

    ):

        super().__init__(
            *args,
            **kwargs
        )

        if "lab" in self.data:

            try:

                lab_id = int(
                    self.data.get(
                        "lab"
                    )
                )

                self.fields[
                    "equipments"
                ].queryset = Equipment.objects.filter(
                    lab_id=lab_id
                )

            except Exception:

                pass

        elif self.initial.get(
            "lab"
        ):

            self.fields[
                "equipments"
            ].queryset = Equipment.objects.filter(
                lab=self.initial["lab"]
            )

    def clean(self):

        cleaned_data = super().clean()

        booking_type = cleaned_data.get(
            "booking_type"
        )

        equipments = cleaned_data.get(
            "equipments"
        )

        from_time = cleaned_data.get(
            "from_time"
        )

        to_time = cleaned_data.get(
            "to_time"
        )

        if (
            from_time
            and
            to_time
            and
            from_time >= to_time
        ):

            raise forms.ValidationError(
                "To Time must be later than From Time."
            )

        if (

            booking_type == "EQUIPMENT"

            and

            not equipments

        ):

            raise forms.ValidationError(

                "Select at least one equipment."

            )

        return cleaned_data


class HallBookingForm(forms.ModelForm):

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

        widgets = {

            "hall": forms.Select(

                attrs={
                    "class": "form-select"
                }

            ),

            "booking_date": forms.DateInput(

                attrs={
                    "type": "date",
                    "class": "form-control"
                }

            ),

            "from_time": forms.TimeInput(

                attrs={
                    "type": "time",
                    "class": "form-control"
                }

            ),

            "to_time": forms.TimeInput(

                attrs={
                    "type": "time",
                    "class": "form-control"
                }

            ),

            "ac": forms.CheckboxInput(

                attrs={
                    "class": "form-check-input"
                }

            ),

            "projector": forms.CheckboxInput(

                attrs={
                    "class": "form-check-input"
                }

            ),

            "seats": forms.NumberInput(

                attrs={
                    "class": "form-control",
                    "min": 0
                }

            ),

            "mic_qty": forms.NumberInput(

                attrs={
                    "class": "form-control",
                    "min": 0
                }

            ),

            "water_bottle_qty": forms.NumberInput(

                attrs={
                    "class": "form-control",
                    "min": 0
                }

            ),

        }

    def clean(self):

        cleaned_data = super().clean()

        hall = cleaned_data.get(
            "hall"
        )

        seats = cleaned_data.get(
            "seats"
        )

        from_time = cleaned_data.get(
            "from_time"
        )

        to_time = cleaned_data.get(
            "to_time"
        )

        if (

            from_time
            and
            to_time
            and
            from_time >= to_time

        ):

            raise forms.ValidationError(

                "To Time must be later than From Time."

            )

        if (

            hall
            and
            seats is not None
            and
            seats > hall.capacity

        ):

            raise forms.ValidationError(

                f"Hall capacity is only {hall.capacity}."

            )

        return cleaned_data