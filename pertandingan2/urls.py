from django.urls import path
from pertandingan2.views import *

app_name = "pertandingan2"

urlpatterns = [
    path("", list_pertandingan, name="list_pertandingan"),
    path("create_pertandingan/", create_pertandingan, name="create_pertandingan"),
    path(
        "create_pertandingan_R32/create_pertandingan_R16/create_pertandingan_PerempatFinal/create_pertandingan_SemiFinal/create_pertandingan_Final/",
        create_pertandingan_Final,
        name="create_pertandingan_Final",
    ),
    path(
        "create_pertandingan_R32/create_pertandingan_R16/create_pertandingan_PerempatFinal/create_pertandingan_SemiFinal/",
        create_pertandingan_SemiFinal,
        name="create_pertandingan_SemiFinal",
    ),
    path(
        "create_pertandingan_R32/create_pertandingan_R16/create_pertandingan_PerempatFinal/",
        create_pertandingan_PerempatFinal,
        name="create_pertandingan_PerempatFinal",
    ),
    path(
        "create_pertandingan_R32/create_pertandingan_R16/",
        create_pertandingan_R16,
        name="create_pertandingan_R16",
    ),
    path(
        "create_pertandingan_R32/",
        create_pertandingan_R32,
        name="create_pertandingan_R32",
    ),
]
