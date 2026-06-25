from django.urls import path

from .views import (
    upload_labs_csv,
    upload_equipment_csv
)

urlpatterns = [

    path(
        "labs/import/",
        upload_labs_csv,
        name="upload_labs_csv"
    ),

    path(
        "equipment/import/",
        upload_equipment_csv,
        name="upload_equipment_csv"
    ),
]