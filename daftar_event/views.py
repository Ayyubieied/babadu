from django.shortcuts import render
from utils.query import *
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
import random
from django.shortcuts import render, redirect
from django.db import connection


def daftar_event1(request):
    # role = request.COOKIES.get('role')

    with connection.cursor() as cursor:
        cursor.execute("SELECT nama, negara, kapasitas FROM stadium")
        stadiums = cursor.fetchall()

    print(stadiums)

    context = {
        'stadiums': stadiums
    }

    return render(request, "daftar_event1.html", context)

def dict_fetch_all(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def daftar_event2(request):
    stadium_name = request.POST.get('stadium_name', '')

    with connection.cursor() as cursor:
        cursor.execute("SELECT nama_event, total_hadiah, tgl_mulai, kategori_superseries "
                       "FROM event WHERE nama_stadium = %s AND tgl_mulai > current_date", [stadium_name])
        events = dict_fetch_all(cursor)  # Fetch all rows as dictionaries

    context = {
        'stadium_name': stadium_name,
        'events': events
    }

    return render(request, "daftar_event2.html", context)

def dict_fetch_one(cursor):
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, cursor.fetchone()))

def kategori(request):
    if request.method == 'POST':
        nama_event = request.POST.get('nama_event')

        # Get event details
        with connection.cursor() as cursor:
            cursor.execute("SELECT nama_event, total_hadiah, tgl_mulai, tgl_selesai, kategori_superseries, stadium.nama, stadium.kapasitas, event.negara "
                           "FROM event "
                           "INNER JOIN stadium ON event.nama_stadium = stadium.nama "
                           "WHERE event.nama_event = %s", [nama_event])
            event_details = cursor.fetchone()

        # Get matches for the selected event
        with connection.cursor() as cursor:
            cursor.execute("SELECT pk.jenis_partai, pk.nama_event, pk.tahun_event, "
                   "ppk.nomor_peserta, pg.id_atlet_ganda "
                   "FROM partai_kompetisi pk "
                   "LEFT JOIN partai_peserta_kompetisi ppk ON pk.jenis_partai = ppk.jenis_partai "
                   "AND pk.nama_event = ppk.nama_event "
                   "AND pk.tahun_event = ppk.tahun_event "
                   "LEFT JOIN peserta_kompetisi p ON ppk.nomor_peserta = p.nomor_peserta "
                   "LEFT JOIN atlet_ganda pg ON p.id_atlet_ganda = pg.id_atlet_ganda "
                   "WHERE pk.nama_event = %s", [nama_event])
            matches = cursor.fetchall()

        context = {
            'nama_event': nama_event,
            'event_details': event_details,
            'matches': matches
        }
        return render(request, 'kategori.html', context)
    else:
        return HttpResponseBadRequest("Invalid request method")


