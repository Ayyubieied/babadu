from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from utils.query import *
from django.db import connection
from authentication.forms import *

import re

# Create your views here.


def show_main(request):
    if request.COOKIES.get('role') is not None:
        return HttpResponseRedirect(reverse('authentication:home'))
    else:


        return render(request, 'landing.html')
    
def register(request):
    return render(request, 'register.html')
        
def register_atlet(request):
    # if request method post, case 
    if (request.method == 'POST'):
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        negara = request.POST.get('negara')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        play = request.POST.get('play')
        tinggi_badan = request.POST.get('tinggi_badan')
        jenis_kelamin = request.POST.get('jenis_kelamin')

        if play == 'left':
            play = 'false'
        else:
            play = 'true'
        
        if(jenis_kelamin == 'L'):
            jenis_kelamin = 'true'
        else:
            jenis_kelamin = 'false'


        if nama == '' or email == '' or negara == '' or tanggal_lahir == '' or play == '' or tinggi_badan == '' or jenis_kelamin == '':
            form = registerFormAtlet(request.POST or None)
            context = {
                'form': form,
                'msg': 'Semua field harus diisi'
            }
            return render(request, 'register-atlet.html', context)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            form = registerFormAtlet(request.POST or None)
            context = {
                'form': form,
                'msg': 'Format email tidak valid'
            }
            return render(request, 'register-atlet.html', context)
        

        
        if not re.match(r"[0-9]{3}", tinggi_badan) or int(tinggi_badan) > 280:
            form = registerFormAtlet(request.POST or None)
            context = {
                'form': form,
                'msg': 'Format tinggi badan tidak valid. Gunakan format XXX cm'
            }
            return render(request, 'register-atlet.html', context)
        
        error, result = try_except_query(f'select register_atlet(\'{email}\',\'{nama}\',\'{tanggal_lahir}\',\'{negara}\',\'{play}\',\'{tinggi_badan}\',\'{jenis_kelamin}\');')
        if error:
            form = registerFormAtlet(request.POST or None)
            context = {
                'form': form,
                'msg': result
            }
            return render(request, 'register-atlet.html', context)
        else:
            form = registerFormAtlet(request.POST or None)
            context = {
                'form': form,
                'success': f'Pendaftaran atlet {nama} berhasil'
            }
            return render(request, 'register-atlet.html', context)
    else:
        form = registerFormAtlet()
        context = {
            'form': form
        }
        return render(request, 'register-atlet.html', context)

def register_umpire(request):

    if request.method == 'POST':
        email= request.POST.get('email')
        nama = request.POST.get('nama')
        negara = request.POST.get('negara')

        if nama == '' or email == '' or negara == '':
            form = registerFormUmpire(request.POST or None) 
            context = {
                'form': form,
                'msg': 'Semua field harus diisi'
            }
            return render(request, 'register-umpire.html', context)

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            form = registerFormUmpire(request.POST or None)
            context = {
                'form': form,   
                'msg': 'Format email tidak valid'
            }
            return render(request, 'register-atlet.html', context)
        error, result = try_except_query(f'insert into member(nama, email) values (\'{nama}\',\'{email}\');');
        if error:
            form = registerFormUmpire(request.POST or None)
            context = {
                'form': form,   
                'msg': result
            }
            return render(request, 'register-umpire.html', context)
        else:
            id_umpire_baru = execute_query(f'SELECT id FROM babadu.member WHERE nama = \'{nama}\' AND email = \'{email}\';')[0][0]
            print(id_umpire_baru)
            execute_query(f'insert into babadu.umpire values (\'{id_umpire_baru}\', \'{negara}\');')
            form = registerFormUmpire(request.POST or None)
            context={
                'success' : f'Pendaftaran umpire {nama} berhasil',
                'form': form,
            }
            return render(request, 'register-umpire.html', context)
    else:
        form = registerFormUmpire()
        context = {
            'form': form
        }
        return render(request, 'register-umpire.html', context)

def register_pelatih(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        negara = request.POST.get('negara')
        kategori = request.POST.getlist('kategori')
        tanggal_mulai = request.POST.get('tanggal_mulai')
        print(nama, email, negara, kategori, tanggal_mulai)
        if nama == '' or email == '' or negara == '' or kategori == '' or tanggal_mulai == '':
            form = registerFormPelatih(request.POST or None)
            context = {
                'form': form,
                'msg': 'Semua field harus diisi'
            }
            return render(request, 'register-pelatih.html', context)
        if not re.match(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", tanggal_mulai):
            form = registerFormAtlet(request.POST or None)
            context = {
                'form': form,
                'msg': 'Format tanggal lahir tidak valid. Gunakan format YYYY-MM-DD'
            }
            return render(request, 'register-atlet.html', context)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            form = registerFormPelatih(request.POST or None)
            context = {
                'form': form,
                'msg': 'Format email tidak valid'
            }
            return render(request, 'register-pelatih.html', context)
        
        error, result = try_except_query(f'insert into member(nama, email) values (\'{nama}\',\'{email}\');');
        if error:
            form = registerFormPelatih(request.POST or None)
            context = {
                'form': form,
                'msg': result
            }
            return render(request, 'register-pelatih.html', context)
        else:
            id_pelatih_baru = execute_query(f'SELECT id FROM babadu.member WHERE nama = \'{nama}\' AND email = \'{email}\';')[0][0]
            execute_query(f'insert into babadu.pelatih values (\'{id_pelatih_baru}\', \'{tanggal_mulai}\');')

            print(id_pelatih_baru)
            for kategori_baru in kategori:
                execute_query(f'insert into babadu.pelatih_spesialisasi values (\'{id_pelatih_baru}\', \'{kategori_baru}\');')
            form = registerFormPelatih(request.POST or None)   

        context = {
            'form': form,
            'success': f'Pendaftaran atlet {nama} berhasil'
        }
        return render(request, 'register-pelatih.html', context)
    else:
        form = registerFormPelatih(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'register-pelatih.html', context)


def login(request):
    if request.COOKIES.get('id') and request.COOKIES.get('role'):
        return HttpResponseRedirect(reverse('authentication:home'))
    
    if request.method == 'POST':
        nama = request.POST.get('nama')
        print(nama)
        email = request.POST.get('email')
        print(email)

        if nama == '' or email == '':
            context = {
                'msg': 'Nama dan email tidak boleh kosong'
            }
            return render(request, 'login.html', context)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            context = {
                'msg': 'Format email tidak valid'
            }
            return render(request, 'login.html', context)
        
        error, result = try_except_query(f'SELECT * FROM babadu.member WHERE nama = \'{nama}\' AND email = \'{email}\';');
        
        if not error:
            if result == []:
                context = {
                    'msg': 'Nama atau email tidak terdaftar'
                }
                return render(request, 'login.html', context)
            
            id_user_login = result[0][0]
            print(id_user_login)
            is_pelatih = execute_query(f'SELECT * FROM babadu.pelatih WHERE id = \'{id_user_login}\';')
            is_umpire = execute_query(f'SELECT * FROM babadu.umpire WHERE id = \'{id_user_login}\';')
            is_atlet = execute_query(f'SELECT * FROM babadu.atlet WHERE id = \'{id_user_login}\';')
            print("masuk")
            response = HttpResponseRedirect(reverse('authentication:home'))
            if is_pelatih != []:
                response.set_cookie('role','pelatih')
            if is_umpire != []:
                response.set_cookie('role','umpire')
            if is_atlet != []:
                response.set_cookie('role','atlet')
                print(id_user_login)
                is_qualified = execute_query(f'select check_atlet(\'{id_user_login}\');')
                print(is_qualified[0][0])

                if is_qualified[0][0] :
                    print("masuk if")
                    response.set_cookie('role','atlet-kualifikasi')

                else:
                    response.set_cookie('role','atlet-non-kualifikasi')


                print(request.COOKIES.get('role2'))
            response.set_cookie('id', result[0][0])
            response.set_cookie('nama', result[0][1])
            response.set_cookie('email', result[0][2])
            return response
        
        else:
            context = {
                'msg': result
            }
            return render(request, 'login.html', context)
    return render(request, 'login.html')

def logout(request):
    response = HttpResponseRedirect(reverse('authentication:show_main'))
    for cookie in request.COOKIES:
        response.delete_cookie(cookie)
    return response

def home(request ):
    if request.COOKIES.get('role') is None:
        return HttpResponseRedirect(reverse('authentication:show_main'))
    
    print(request.COOKIES.get('role'))
    role = request.COOKIES.get('role')
    id = request.COOKIES.get('id')
    nama = request.COOKIES.get('nama')
    email = request.COOKIES.get('email')
    if "atlet" in role:
        data_atlet = execute_query(f'SELECT * FROM babadu.atlet WHERE id = \'{id}\';')[0]
        play =  "Kanan" if data_atlet[3] == True else "Kiri"

        jenis_kelamin = "Laki-laki" if data_atlet[6] == True else "Perempuan"

        status = "Not Qualified" if "non" in role else "Qualified"

        world_rank = data_atlet[5] if data_atlet[5] != None else "-"

        total_point = execute_query(f'select sum(total_point) from point_history where id_atlet = \'{id}\';')[0]
        total_point = total_point[0] if total_point[0]!= None else "-"

        pelatih = execute_query(f'select string_agg(nama, \', \') from member where id in (select id_pelatih from atlet_pelatih where id_atlet = \'{id}\');')[0][0]
        pelatih = pelatih if pelatih != None else "-"  

     
        context = {
        'role': role,
        'id': id,
        'nama': nama,
        'negara': data_atlet[2],
        'email': email,
        'tgl_lahir': data_atlet[1],
        'play': play,
        'tinggi_badan': str(data_atlet[4]) + " cm",
        'jenis_kelamin': jenis_kelamin,
        'pelatih': pelatih,
        'status': status,
        'world_rank': world_rank,
        'total_point': total_point,
        }
        return render(request, 'home.html',context)

    elif role == 'umpire':
        data_umpire = execute_query(f'SELECT * FROM babadu.umpire WHERE id = \'{id}\';')[0]
        context = {
        'role': role,
        'id': id,
        'nama': nama,
        'email': email,
        'negara': data_umpire[1],
         }
        return render(request, 'home.html',context)
        
    else:
        tanggal_mulai = execute_query(f'SELECT tanggal_mulai FROM babadu.pelatih WHERE id = \'{id}\';')[0][0]
        spesialisasi = execute_query(f'select string_agg(spesialisasi, \', \') from pelatih_spesialisasi, spesialisasi where id_pelatih = \'{id}\'and id_spesialisasi = id;')[0]
        spesialisasi_string = ""
        for i in range(len(spesialisasi)):
            spesialisasi_string +=  spesialisasi[i]
        spesialisasi_string = spesialisasi_string if spesialisasi_string != "" else "-"
        context = {
        'role': role,
        'id': id,
        'nama': nama,
        'email': email,
        'tanggal_mulai': tanggal_mulai, 
        'spesialisasi': spesialisasi_string,
        }
        return render(request, 'home.html',context)