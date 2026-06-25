from django import forms


class StartupLoginForm(forms.Form):

    startup_id = forms.CharField(
        max_length=4
    )

    password = forms.CharField(
        widget=forms.PasswordInput
    )