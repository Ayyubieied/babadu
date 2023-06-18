from django.urls import path
from daftar_event.views import daftar_event1, daftar_event2, kategori

app_name = 'daftar_event'

urlpatterns = [
    path('daftar_event1/', daftar_event1, name='daftar_event1'),
    path('daftar_event2/', daftar_event2, name='daftar_event2'),
    path('kategori/', kategori, name='kategori'),
]
