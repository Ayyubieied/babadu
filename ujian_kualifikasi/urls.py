from django.urls import path
from authentication.views import *
from ujian_kualifikasi.views import *
    
appname='ujian_kualifkiasi'
urlpatterns = [
    path('', show_ujian, name='show_ujian'),
    path('create/', create_ujian, name='create_ujian'),
    path('riwayat/', show_riwayat, name='show_riwayat'),
    path('ujian/', show_soal, name='show_soal'),
    path('hasil/', show_hasil_ujian, name='show_hasil_ujian'),
    path('check/<int:tahun>/<int:batch>/<str:tempat>/<str:tanggal>/', check_ujian, name='check_ujian')

]