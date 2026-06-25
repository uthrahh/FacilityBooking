import csv

from halls.models import Hall


def import_halls(
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

            Hall.objects.create(
                hall_id=row["hall_id"],
                name=row["name"],
                capacity=row[
                    "capacity"
                ]
            )