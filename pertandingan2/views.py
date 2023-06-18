from audioop import reverse
from collections import namedtuple
import datetime
from multiprocessing import connection
from urllib import request
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.db import connection

from collections import namedtuple
import datetime
from django.utils import timezone


def list_pertandingan(request):
    cursor = connection.cursor()
    cursor.execute(
        f"""
            SELECT * FROM event;
        """
    )
    event = cursor.fetchall()

    list_event = []
    for i in event:
        list_event.append(i)
    context = {"events": list_event}
    connection.close()
    return render(request, "list_pertandingan.html", context)


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple("Data", [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def get_query(str):
    """Execute SQL query and return its result as a list"""
    cursor = connection.cursor()
    result = []
    try:
        cursor.execute(str)
        result = namedtuplefetchall(cursor)
    except Exception as e:
        # print(e)
        # result = e;
        result = [e]
    finally:
        cursor.close()
        return result


def create_pertandingan(request):
    # role_user = request.COOKIES.get("role")
    # if role_user == "umpire":
    # id = request.COOKIES.get("id")
    id = "99186252-e8a8-11ed-a05b-0242ac120003"
    cursor = connection.cursor()
    cursor.execute(
        f"""
                SELECT * FROM EVENT WHERE nama_event = 'EventA' AND tahun = '2023';
            """
    )
    event = cursor.fetchall()
    data_event = []
    for i in event:
        data_event.append(i)

    id_umpire = id
    tanggal = data_event[0][4]
    waktu_mulai = timezone.now()
    total_durasi = 0
    nama_event = data_event[0][0]
    tahun_event = data_event[0][1]

    cursor = connection.cursor()
    cursor.execute(
        f"SELECT nomor_peserta FROM peserta_mendaftar_event WHERE nama_event = %s  AND tahun = %s ",
        [nama_event, tahun_event],
    )
    peserta = cursor.fetchall()
    connection.close()

    jumlah_tim_bermain = len(peserta)
    if jumlah_tim_bermain > 16:
        jenis_babak = "R32"
    elif jumlah_tim_bermain > 8:
        jenis_babak = "R16"
    elif jumlah_tim_bermain > 4:
        jenis_babak = "Perempat Final"
    elif jumlah_tim_bermain == 3:
        jenis_babak = "SemiFinal"
    else:
        jenis_babak = "Final"

    # cursor = connection.cursor()
    # cursor.execute(
    #     f"""
    #             INSERT INTO MATCH VALUES (
    #             ('{jenis_babak}',
    #             '{tanggal}',
    #             '{waktu_mulai}',
    #             '{total_durasi}',
    #             '{nama_event}',
    #             '{tahun_event}',
    #             '{id_umpire}',
    #             """
    # )
    # connection.commit()

    match = [
        jenis_babak,
        tanggal,
        waktu_mulai,
        total_durasi,
        nama_event,
        tahun_event,
        id_umpire,
    ]
    list_peserta_mengikuti_match = []

    # KIRIM KE KAWUNG PESERTA_MENGIKUTI_MATCH
    for i in peserta:
        nomor_peserta = i
        status_menang = 0
        # cursor = connection.cursor()
        # cursor.execute(
        #     f"""
        #         INSERT INTO peserta_mengikuti_match VALUES (
        #         ('{jenis_babak}',
        #         '{tanggal}',
        #         '{waktu_mulai}',
        #         '{nomor_peserta}',
        #         '{status_menang}',
        #         """
        # )
        # connection.commit()

        # MENENTUKAN TIM ATAU INDIVIDU
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT id_atlet_ganda,id_atlet_kualifikasi  FROM peserta_kompetisi WHERE nomor_peserta = %s ",
            nomor_peserta,
        )
        id_atlet = cursor.fetchall()

        # cursor = connection.cursor()
        # cursor.execute(
        #     f"SELECT id_atlet_ganda FROM peserta_kompetisi WHERE nomor_peserta = %s ",
        #     nomor_peserta,
        # )
        # id_atlet_ganda = cursor.fetchall()
        # # connection.close()

        # cursor.execute(
        #     f"SELECT id_atlet_kualifikasi FROM peserta_kompetisi WHERE nomor_peserta = %s ",
        #     nomor_peserta,
        # )
        # id_atlet_kualifikasi = cursor.fetchall()

        data_satu_peserta_match = []
        id_atlet_ganda = id_atlet[0][0]
        id_atlet_kualifikasi = id_atlet[0][1]

        if id_atlet_ganda != None:
            atlet_ganda = []
            cursor.execute(
                f"SELECT id_atlet_kualifikasi, id_atlet_kualifikasi_2 FROM ATLET_GANDA WHERE id_atlet_ganda = %s ",
                [id_atlet_ganda],
            )
            id_atlet_ganda = cursor.fetchall()
            for id_atlet in id_atlet_ganda:
                cursor.execute(
                    f"SELECT * FROM MEMBER m  JOIN ATLET_kualifikasi a ON m.ID=a.id_atlet WHERE id_atlet= %s ",
                    [id_atlet[0]],
                )
                atlet = cursor.fetchall()
                atlet_ganda.append(atlet)
            data_satu_peserta_match.append(atlet_ganda)
        else:
            cursor.execute(
                f"SELECT * FROM  MEMBER m  JOIN ATLET_kualifikasi a ON m.ID=a.id_atlet WHERE id_atlet= %s ",
                [id_atlet_kualifikasi],
            )
            atlet_kualifikasi = cursor.fetchall()
            data_satu_peserta_match.append(atlet_kualifikasi)

        list_peserta_mengikuti_match.append(data_satu_peserta_match)

    list_pasangan_match = []
    for i in (0, len(list_peserta_mengikuti_match), 2):
        # tim = []
        # tim.append(i)
        # tim.append(i + 1)
        list_peserta_mengikuti_match.append(i)
    context = {
        "data_event": data_event,
        "match": match,
        "list_peserta_match": list_peserta_mengikuti_match,
        "jumlah_peserta": len(list_peserta_mengikuti_match),
        "list_pasangan_match": list_pasangan_match,
    }
    connection.close()
    if jenis_babak == "R32":
        return render(request, "create_pertandingan_R32.html", context)
    elif jenis_babak == "R16":
        return render(request, "create_pertandingan_R16.html", context)
    elif jenis_babak == "Perempat Final":
        return render(request, "create_pertandingan_PerempatFinal.html", context)
    elif jenis_babak == "SemiFinal":
        return render(request, "create_pertandingan_SemiFinal.html", context)
    else:
        return render(request, "create_pertandingan_Final.html", context)


# else:
#     # show 404 page
#     return HttpResponseRedirect(reverse("authentication:show_main"))


def create_match(request):
    # TAMBAHIN ROLE AUTH
    id = request.COOKIES.get("id")
    event = get_query(
        "SELECT * FROM EVENT WHERE nama_event = 'EventA' AND tahun = '2023';"
    )
    # INISIASI MATCH
    id_umpire = id
    tanggal = datetime.date.now()
    waktu_mulai = datetime.timezone.now()
    total_durasi = 0
    nama_event = event.nama_event
    tahun_event = event.tahun
    peserta = get_query(
        f"SELECT nomor_peserta FROM peserta_mendaftar_event WHERE nama_event = %s  AND tahun_event = %s ",
        [nama_event, tahun_event],
    )
    jumlah_tim_bermain = len(peserta)
    if jumlah_tim_bermain > 16:
        jenis_babak = "R32"
    elif jumlah_tim_bermain > 8:
        jenis_babak = "R16"
    elif jumlah_tim_bermain > 4:
        jenis_babak = "Perempat Final"
    elif jumlah_tim_bermain == 3:
        jenis_babak = "SemiFinal"
    else:
        jenis_babak = "Final"

    # KIRIM MATCH KE KAWUNG
    cursor = connection.cursor()
    cursor.execute(
        f"""
            INSERT INTO MATCH VALUES (
            ('{jenis_babak}',
            '{tanggal}',
            '{waktu_mulai}',
            '{total_durasi}',
            '{nama_event}',
            '{tahun_event}',                
            '{id_umpire}',
            """
    )
    connection.commit()

    match = [
        jenis_babak,
        tanggal,
        waktu_mulai,
        total_durasi,
        nama_event,
        tahun_event,
        id_umpire,
    ]
    list_peserta_match = []

    # KIRIM KE KAWUNG PESERTA_MENGIKUTI_MATCH
    for i in peserta:
        nomor_peserta = i
        status_menang = 0
        cursor = connection.cursor()
        cursor.execute(
            f"""
            INSERT INTO peserta_mengikuti_match VALUES (
            ('{jenis_babak}',
            '{tanggal}',
            '{waktu_mulai}',
            '{nomor_peserta}',
            '{status_menang}',
            """
        )
        connection.commit()

        # MENENTUKAN TIM ATAU INDIVIDU
        id_atlet_ganda = get_query(
            f"SELECT id_atlet_ganda FROM peserta_kompetisi WHERE nomor_peserta = %s ",
            nomor_peserta,
        )

        id_atlet_kualifikasi = get_query(
            f"SELECT id_atlet_kualifikasi FROM peserta_kompetisi WHERE nomor_peserta = %s ",
            nomor_peserta,
        )

        id_satu_peserta_match = []

        if len(id_atlet_ganda) > len(id_atlet_kualifikasi):
            id_atlet_ganda = get_query(
                f"SELECT id_atlet_kualifikasi, id_atlet_kualifikasi_2 FROM ATLET_GANDA WHERE id_atlet_ganda = %s ",
                id_atlet_ganda[0],
            )
            for atlet in id_atlet_ganda:
                id_satu_peserta_match.append(atlet)
        else:
            id_satu_peserta_match.append(id_atlet_kualifikasi[0])

        # MENCARI NAMA ATLET DI TIM
        data_satu_peserta_match = []
        for i in id_satu_peserta_match:
            id = i
            nama_atlet = get_query(f"SELECT nama FROM MEMBER WHERE id = %s ", id)
            atlet = [id, nama_atlet[0]]
            data_satu_peserta_match.append(atlet)

        list_peserta_match.append(data_satu_peserta_match)

    for i in list_peserta_match:
        tim = []
        tim.append(i)
        tim.append(i + 1)

    # UNTUK DI PASS KE HTML

    context = {
        # "data_event" :
        "match": match,
        "list_peserta_match": list_peserta_match,
        "jumlah_peserta": len(list_peserta_match),
        # list_peserta = [[a,b],[c,d]]
        #
        # event,
    }
    return render(request, "show_pertandingan_sql.html", context)


def next_pertandingan(request):
    # def update_pertandingan(request):
    #     # Perform necessary database operations and calculations

    #     # Generate the updated HTML table for the pertandingan
    #     updated_html_table = (
    #         generate_updated_html_table()
    #     )  # Replace with your own implementation

    #     # Prepare the JSON response
    #     response = {
    #         "html_table": updated_html_table,
    #     }

    #     return JsonResponse(response)
    return render(request, "update_match.html")


def create_pertandingan_PerempatFinal(request):
    # role_user = request.COOKIES.get("role")
    # if role_user == "umpire":
    # id = request.COOKIES.get("id")
    id = "99186252-e8a8-11ed-a05b-0242ac120003"
    cursor = connection.cursor()
    cursor.execute(
        f"""
                SELECT * FROM EVENT WHERE nama_event = 'EventA' AND tahun = '2023';
            """
    )
    event = cursor.fetchall()
    data_event = []
    for i in event:
        data_event.append(i)

    id_umpire = id
    tanggal = data_event[0][4]
    waktu_mulai = timezone.now()
    total_durasi = 0
    nama_event = data_event[0][0]
    tahun_event = data_event[0][1]

    cursor = connection.cursor()
    cursor.execute(
        f"SELECT nomor_peserta FROM peserta_mendaftar_event WHERE nama_event = %s  AND tahun = %s ",
        [nama_event, tahun_event],
    )
    peserta = cursor.fetchall()
    connection.close()

    jumlah_tim_bermain = len(peserta)
    if jumlah_tim_bermain > 16:
        jenis_babak = "R32"
    elif jumlah_tim_bermain > 8:
        jenis_babak = "R16"
    elif jumlah_tim_bermain > 4:
        jenis_babak = "Perempat Final"
    elif jumlah_tim_bermain == 3:
        jenis_babak = "SemiFinal"
    else:
        jenis_babak = "Final"

    # cursor = connection.cursor()
    # cursor.execute(
    #     f"""
    #             INSERT INTO MATCH VALUES (
    #             ('{jenis_babak}',
    #             '{tanggal}',
    #             '{waktu_mulai}',
    #             '{total_durasi}',
    #             '{nama_event}',
    #             '{tahun_event}',
    #             '{id_umpire}',
    #             """
    # )
    # connection.commit()

    match = [
        jenis_babak,
        tanggal,
        waktu_mulai,
        total_durasi,
        nama_event,
        tahun_event,
        id_umpire,
    ]
    list_peserta_mengikuti_match = []

    # KIRIM KE KAWUNG PESERTA_MENGIKUTI_MATCH
    for i in peserta:
        nomor_peserta = i
        status_menang = 0
        # cursor = connection.cursor()
        # cursor.execute(
        #     f"""
        #         INSERT INTO peserta_mengikuti_match VALUES (
        #         ('{jenis_babak}',
        #         '{tanggal}',
        #         '{waktu_mulai}',
        #         '{nomor_peserta}',
        #         '{status_menang}',
        #         """
        # )
        # connection.commit()

        # MENENTUKAN TIM ATAU INDIVIDU
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT id_atlet_ganda,id_atlet_kualifikasi  FROM peserta_kompetisi WHERE nomor_peserta = %s ",
            nomor_peserta,
        )
        id_atlet = cursor.fetchall()

        # cursor = connection.cursor()
        # cursor.execute(
        #     f"SELECT id_atlet_ganda FROM peserta_kompetisi WHERE nomor_peserta = %s ",
        #     nomor_peserta,
        # )
        # id_atlet_ganda = cursor.fetchall()
        # # connection.close()

        # cursor.execute(
        #     f"SELECT id_atlet_kualifikasi FROM peserta_kompetisi WHERE nomor_peserta = %s ",
        #     nomor_peserta,
        # )
        # id_atlet_kualifikasi = cursor.fetchall()

        data_satu_peserta_match = []
        id_atlet_ganda = id_atlet[0][0]
        id_atlet_kualifikasi = id_atlet[0][1]

        if id_atlet_ganda != None:
            atlet_ganda = []
            cursor.execute(
                f"SELECT id_atlet_kualifikasi, id_atlet_kualifikasi_2 FROM ATLET_GANDA WHERE id_atlet_ganda = %s ",
                [id_atlet_ganda],
            )
            id_atlet_ganda = cursor.fetchall()
            for id_atlet in id_atlet_ganda:
                cursor.execute(
                    f"SELECT * FROM MEMBER m  JOIN ATLET_kualifikasi a ON m.ID=a.id_atlet WHERE id_atlet= %s ",
                    [id_atlet[0]],
                )
                atlet = cursor.fetchall()
                atlet_ganda.append(atlet)
            data_satu_peserta_match.append(atlet_ganda)
        else:
            cursor.execute(
                f"SELECT * FROM  MEMBER m  JOIN ATLET_kualifikasi a ON m.ID=a.id_atlet WHERE id_atlet= %s ",
                [id_atlet_kualifikasi],
            )
            atlet_kualifikasi = cursor.fetchall()
            data_satu_peserta_match.append(atlet_kualifikasi)

        list_peserta_mengikuti_match.append(data_satu_peserta_match)

    list_pasangan_match = []
    for i in (0, len(list_peserta_mengikuti_match), 2):
        # tim = []
        # tim.append(i)
        # tim.append(i + 1)
        list_peserta_mengikuti_match.append(i)
    context = {
        "data_event": data_event,
        "match": match,
        "list_peserta_match": list_peserta_mengikuti_match,
        "jumlah_peserta": len(list_peserta_mengikuti_match),
        "list_pasangan_match": list_pasangan_match,
    }

    return render(request, "create_pertandingan_PerempatFinal.html", context)


def create_pertandingan_SemiFinal(request):
    return render(request, "create_pertandingan_SemiFinal.html")


def create_pertandingan_Final(request):
    return render(request, "create_pertandingan_Final.html")


def create_pertandingan_R16(request):
    return render(request, "create_pertandingan_R16.html")


def create_pertandingan_R32(request):
    return render(request, "create_pertandingan_R32.html")
