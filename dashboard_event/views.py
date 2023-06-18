from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from utils.query import *
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

# Create your views here.
    
@csrf_exempt
def create_sponsor(request):
    if request.method == "POST":

        user_id = request.COOKIES.get('id')
        nama_sponsor = request.POST.get('sponsor-selector')
        tanggal_mulai = request.POST.get('tanggal-mulai')
        tanggal_selesai = request.POST.get('tanggal-selesai')
        # Process the input data as needed
        # formatted_mulai = datetime.strptime(tanggal_mulai, '%m/%d/%Y')
        # formatted_selesai = datetime.strptime(tanggal_selesai, '%m/%d/%Y')

        print(user_id)
        print(tanggal_mulai)
        print(tanggal_selesai)

        # cursor.execute(f'insert into ujian_kualifikasi values({user_id}, {nama_sponsor}, \'{tanggal_mulai}\', \'{tanggal_selesai}\');')

        query = f"""
            INSERT INTO ATLET_SPONSOR(ID_Atlet, ID_Sponsor, Tgl_mulai, Tgl_selesai) 
            VALUES ('{user_id}', '{nama_sponsor}', '{tanggal_mulai}', '{tanggal_selesai}');
        """

        cursor.execute(query)
        connection.commit()

        # response = {'data': data}
        # print(response)

        return redirect('dashboard_event:read_sponsor')
    
        # return render(request, 'create_sponsor.html')
    else:
        return render(request, 'create_sponsor.html')

# def insert_sponsor(request):

def logout(request):
    response = HttpResponseRedirect(reverse('show_main'))
    for cookie in request.COOKIES:
        response.delete_cookie(cookie)
    return response

def enrolled_partai(request):
    id = request.COOKIES.get('id')
    with connection.cursor() as cursor:
        cursor.execute(f'''
        SELECT e.nama_event, e.tahun, e.nama_stadium, ppk.jenis_partai, e.kategori_superseries, e.tgl_mulai, e.tgl_selesai
        FROM babadu.event AS e
        JOIN babadu.peserta_mendaftar_event AS pme ON pme.nama_event = e.nama_event AND pme.tahun = e.tahun
        JOIN babadu.peserta_kompetisi AS pk ON pk.nomor_peserta = pme.nomor_peserta
        JOIN babadu.partai_peserta_kompetisi AS ppk ON pk.nomor_peserta = ppk.nomor_peserta AND ppk.nama_event = e.nama_event AND ppk.tahun_event = e.tahun
        JOIN babadu.atlet_ganda AS ag ON pk.id_atlet_ganda = ag.id_atlet_ganda AND pk.id_atlet_kualifikasi = ag.id_atlet_kualifikasi
        WHERE ag.id_atlet_kualifikasi = '991875b2-e8a8-11ed-a05b-0242ac120003'
        OR ag.id_atlet_kualifikasi_2 = '991875b2-e8a8-11ed-a05b-0242ac120003';


        ''')
        table_data = cursor.fetchall()

    # Pass the table data to the HTML template
    context = {
        'table_data': table_data
    }

    return render(request, 'enrolled_partai.html', context)


def enrolled_event_table(request):
    # Execute the SQL query
    id = request.COOKIES.get('id')
    with connection.cursor() as cursor:
        cursor.execute(f'''
            SELECT e.nama_event, e.tahun, e.nama_stadium, e.kategori_superseries, e.tgl_mulai, e.tgl_selesai
            FROM babadu.event AS e JOIN babadu.peserta_mendaftar_event AS pme ON pme.nama_event = e.nama_event AND pme.tahun = e.tahun 
            JOIN babadu.peserta_kompetisi AS pk ON pk.nomor_peserta = pme.nomor_peserta
            JOIN babadu.atlet_ganda AS ag ON pk.id_atlet_ganda = ag.id_atlet_ganda AND pk.id_atlet_kualifikasi = ag.id_atlet_kualifikasi
            WHERE ag.id_atlet_kualifikasi = '{id}' 
            OR ag.id_atlet_kualifikasi_2 = '{id}';
        ''')
        
        table_event = cursor.fetchall()

    # Pass the table data to the HTML template
    context = {
        'table_event': table_event
    }

    return render(request, 'enrolled_event.html', context)

def read_sponsor(request):
    # Execute the SQL query
    id = request.COOKIES.get('id')
    with connection.cursor() as cursor:
        cursor.execute(f'''
            SELECT s.nama_brand, sp.tgl_mulai, sp.tgl_selesai
            FROM babadu.sponsor AS s, babadu.atlet_sponsor AS sp, babadu.atlet AS a, babadu.member AS m
            WHERE sp.id_atlet = '{id}' 
            AND sp.id_sponsor = s.id
            AND sp.id_atlet = a.id
            AND a.id = m.id;
        ''')
        table_sponsor = cursor.fetchall()

    # Pass the table data to the HTML template
    context = {
        'table_sponsor': table_sponsor
    }
    print(context)

    return render(request, 'read_sponsor.html', context)

def sponsor_card(request):
    # Execute the SQL query
    id = request.COOKIES.get('id')
    with connection.cursor() as cursor:
        cursor.execute(f'''
            SELECT s.nama_brand, sp.tgl_mulai, sp.tgl_selesai
            FROM babadu.sponsor AS s, babadu.atlet_sponsor AS sp, babadu.atlet AS a, babadu.member AS m
            WHERE sp.id_atlet = '{id}' 
            AND sp.id_sponsor = s.id
            AND sp.id_atlet = a.id
            AND a.id = m.id;
        ''')
        table_sponsor = cursor.fetchall()

    # Pass the table data to the HTML template
    context = {
        'table_sponsor': table_sponsor
    }
    print(context)

    return render(request, 'sponsor_card.html', context)