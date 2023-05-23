from django.urls import path
from authentication.views import *


appname='authentication'
urlpatterns = [
    path('', show_main, name='show_main'),
    path('login/', login, name='login'),
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('register/pelatih/', register_pelatih, name='register_pelatih'),
    path('register/umpire/', register_umpire, name='register_umpire'),
    path('register/atlet/', register_atlet, name='register_atlet'),
    path('logout/', logout, name='logout'),
]