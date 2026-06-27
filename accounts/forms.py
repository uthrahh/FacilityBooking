from django import forms
from django.core.validators import RegexValidator

from startups.models import Startup


startup_id_validator = RegexValidator(
    regex=r"^\d{4}$",
    message="Startup ID must contain exactly 4 digits."
)


class StartupLoginForm(forms.Form):

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
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password"
            }
        )
    )


class StartupSignupForm(forms.ModelForm):

    startup_id = forms.CharField(
        validators=[
            startup_id_validator
        ],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "maxlength": "4",
                "placeholder": "1503"
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
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ),
        required=False
    )

    class Meta:

        model = Startup

        fields = [

            "startup_id",

            "name",

            "email",

            "phone",

        ]


class AdminLoginForm(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
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