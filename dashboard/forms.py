from django import forms

from startups.models import Startup
from labs.models import Lab
from labs.models import Equipment
from halls.models import Hall


class StartupForm(forms.ModelForm):

    class Meta:

        model = Startup

        fields = [
            "startup_id",
            "name",
            "founder_name",
            "email",
            "phone",
            "incubation_status",
            "password_hash",
            "is_active"
        ]


class LabForm(forms.ModelForm):

    class Meta:

        model = Lab

        fields = "__all__"


class EquipmentForm(forms.ModelForm):

    class Meta:

        model = Equipment

        fields = "__all__"


class HallForm(forms.ModelForm):

    class Meta:

        model = Hall

        fields = "__all__"