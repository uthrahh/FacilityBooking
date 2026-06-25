import csv
import io

from django.shortcuts import (
    render,
    redirect
)

from .forms import (
    HallCSVUploadForm
)

from .models import Hall

def upload_halls_csv(
    request
):

    if request.method == "POST":

        form = HallCSVUploadForm(
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

                Hall.objects.update_or_create(
                    hall_id=row["hall_id"],
                    defaults={
                        "name":
                        row["name"],

                        "capacity":
                        row["capacity"]
                    }
                )

            return redirect(
                "/admin/"
            )

    else:

        form = HallCSVUploadForm()

    return render(
        request,
        "halls/upload_halls.html",
        {
            "form": form
        }
    )