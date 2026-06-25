from django import forms


class HallCSVUploadForm(forms.Form):

    csv_file = forms.FileField()