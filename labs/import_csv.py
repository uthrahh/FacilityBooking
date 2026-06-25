import csv

from labs.models import (
    Lab,
    Equipment
)


def import_labs(
    file_path
):

    with open(
        file_path,
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(
            file
        )

        for row in reader:

            Lab.objects.create(
                lab_id=row["lab_id"],
                name=row["name"]
            )


def import_equipment(
    file_path
):

    with open(
        file_path,
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(
            file
        )

        for row in reader:

            lab = Lab.objects.get(
                lab_id=row["lab_id"]
            )

            Equipment.objects.create(
                equipment_id=row[
                    "equipment_id"
                ],
                name=row["name"],
                lab=lab,
                fee_per_hour=row[
                    "fee_per_hour"
                ]
            )