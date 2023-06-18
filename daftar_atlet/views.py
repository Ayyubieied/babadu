from django.shortcuts import render
from utils.query import *

# Create your views here.
def show_daftar_atlet(request):
    return render(request, "daftar_atlet.html")