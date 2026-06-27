from django import forms
from django.core.validators import RegexValidator

from startups.models import Startup
from labs.models import (
    Lab,
    Equipment,
)
from halls.models import Hall


lab_id_validator = RegexValidator(
    regex=r"^L\d{2}$",
    message="Lab ID must be in the format L01."
)

equipment_id_validator = RegexValidator(
    regex=r"^L\d{2}E\d{2}$",
    message="Equipment ID must be in the format L01E01."
)

hall_id_validator = RegexValidator(
    regex=r"^H\d{2}$",
    message="Hall ID must be in the format H01."
)

startup_id_validator = RegexValidator(
    regex=r"^\d{4}$",
    message="Startup ID must contain exactly 4 digits."
)


class StartupForm(forms.ModelForm):

    startup_id = forms.CharField(
        validators=[
            startup_id_validator
        ]
    )

    class Meta:

        model = Startup

        fields = [

            "startup_id",

            "name",

            "email",

            "phone",

            "is_active",

        ]

        widgets = {

            "startup_id": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),

        }


class LabForm(forms.ModelForm):

    lab_id = forms.CharField(
        validators=[
            lab_id_validator
        ]
    )

    class Meta:

        model = Lab

        fields = [

            "lab_id",

            "name",

            "description",

            "is_active",

        ]

        widgets = {

            "lab_id": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),

        }


class EquipmentForm(forms.ModelForm):

    equipment_id = forms.CharField(
        validators=[
            equipment_id_validator
        ]
    )

    class Meta:

        model = Equipment

        fields = [

            "equipment_id",

            "name",

            "lab",

            "fee_per_hour",

            "is_active",

        ]

        widgets = {

            "equipment_id": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "lab": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "fee_per_hour": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01"
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),

        }


class HallForm(forms.ModelForm):

    hall_id = forms.CharField(
        validators=[
            hall_id_validator
        ]
    )

    class Meta:

        model = Hall

        fields = [

            "hall_id",

            "name",

            "capacity",

            "description",

            "is_active",

        ]

        widgets = {

            "hall_id": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "capacity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),

      }