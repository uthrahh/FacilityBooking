import csv
import io

from django.shortcuts import render
from django.shortcuts import redirect

from .forms import (
    LabCSVUploadForm,
    EquipmentCSVUploadForm
)

from .models import (
    Lab,
    Equipment
)
def upload_labs_csv(
    request
):

    if request.method == "POST":

        form = LabCSVUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            csv_file = request.FILES[
                "csv_file"
            ]

            data = csv_file.read().decode(
                "utf-8"
            )

            reader = csv.DictReader(
                io.StringIO(data)
            )

            for row in reader:

                Lab.objects.update_or_create(
                    lab_id=row["lab_id"],
                    defaults={
                        "name":
                        row["name"]
                    }
                )

            return redirect(
                "/admin/"
            )

    else:

        form = LabCSVUploadForm()

    return render(
        request,
        "labs/upload_labs.html",
        {
            "form": form
        }
    )

def upload_equipment_csv(
    request
):

    if request.method == "POST":

        form = EquipmentCSVUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            csv_file = request.FILES[
                "csv_file"
            ]

            data = csv_file.read().decode(
                "utf-8"
            )

            reader = csv.DictReader(
                io.StringIO(data)
            )

            for row in reader:

                lab = Lab.objects.get(
                    lab_id=row["lab_id"]
                )

                Equipment.objects.update_or_create(
                    equipment_id=row[
                        "equipment_id"
                    ],
                    defaults={
                        "name":
                        row["name"],

                        "lab":
                        lab,

                        "fee_per_hour":
                        row[
                            "fee_per_hour"
                        ]
                    }
                )

            return redirect(
                "/admin/"
            )

    else:

        form = EquipmentCSVUploadForm()

    return render(
        request,
        "labs/upload_equipment.html",
        {
            "form": form
        }
    )