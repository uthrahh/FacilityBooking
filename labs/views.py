import csv
import io

from django.contrib import messages

from django.shortcuts import render
from django.shortcuts import redirect

from .forms import (
    LabCSVUploadForm,
    EquipmentCSVUploadForm,
)

from .models import (
    Lab,
    Equipment,
)

from accounts.decorators import (
    admin_login_required,
)


@admin_login_required
def upload_labs_csv(request):

    form = LabCSVUploadForm(
        request.POST or None,
        request.FILES or None
    )

    if request.method == "POST" and form.is_valid():

        csv_file = request.FILES["csv_file"]

        data = csv_file.read().decode(
            "utf-8"
        )

        reader = csv.DictReader(
            io.StringIO(data)
        )

        count = 0

        for row in reader:

            if not row.get("lab_id"):
                continue

            Lab.objects.update_or_create(

                lab_id=row["lab_id"].strip(),

                defaults={

                    "name": row["name"].strip()

                }

            )

            count += 1

        messages.success(
            request,
            f"{count} Labs Imported Successfully."
        )

        return redirect(
            "lab_list"
        )

    return render(

        request,

        "labs/upload_labs.html",

        {
            "form": form
        }

    )


@admin_login_required
def upload_equipment_csv(request):

    form = EquipmentCSVUploadForm(
        request.POST or None,
        request.FILES or None
    )

    if request.method == "POST" and form.is_valid():

        csv_file = request.FILES["csv_file"]

        data = csv_file.read().decode(
            "utf-8"
        )

        reader = csv.DictReader(
            io.StringIO(data)
        )

        count = 0

        for row in reader:

            try:

                lab = Lab.objects.get(

                    lab_id=row["lab_id"].strip()

                )

            except Lab.DoesNotExist:

                continue

            Equipment.objects.update_or_create(

                equipment_id=row["equipment_id"].strip(),

                defaults={

                    "name": row["name"].strip(),

                    "lab": lab,

                    "fee_per_hour": row["fee_per_hour"]

                }

            )

            count += 1

        messages.success(

            request,

            f"{count} Equipment Imported Successfully."

        )

        return redirect(
            "equipment_list"
        )

    return render(

        request,

        "labs/upload_equipment.html",

        {
            "form": form
        }

    )