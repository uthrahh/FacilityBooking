from django import forms
from django.core.validators import RegexValidator

from .models import Startup


startup_id_validator = RegexValidator(
    regex=r"^\d{4}$",
    message="Startup ID must contain exactly 4 digits."
)


class StartupForm(forms.ModelForm):

    startup_id = forms.CharField(
        label="Startup ID",
        max_length=4,
        validators=[
            startup_id_validator
        ],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "1503",
                "maxlength": "4"
            }
        )
    )

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "9876543210"
            }
        )
    )

    class Meta:

        model = Startup

        fields = [
            "startup_id",
            "name",
            "email",
            "phone",
        ]


class StartupSignupForm(forms.ModelForm):

    startup_id = forms.CharField(
        label="Startup ID",
        max_length=4,
        validators=[
            startup_id_validator
        ],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "1503",
                "maxlength": "4"
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:

        model = Startup

        fields = [
            "startup_id",
            "name",
            "email",
            "phone",
        ]

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get(
            "password"
        )

        confirm_password = cleaned_data.get(
            "confirm_password"
        )

        if (
            password
            and
            confirm_password
            and
            password != confirm_password
        ):
            raise forms.ValidationError(
                "Passwords do not match."
            )

        return cleaned_data