from django import forms


class LabCSVUploadForm(forms.Form):

    csv_file = forms.FileField()


class EquipmentCSVUploadForm(forms.Form):

    csv_file = forms.FileField()