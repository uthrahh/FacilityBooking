from django.urls import path

from .views import (
    upload_halls_csv
)

urlpatterns = [

    path(
        "halls/import/",
        upload_halls_csv,
        name="upload_halls_csv"
    ),
]