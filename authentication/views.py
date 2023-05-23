from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from utils.query import *
from django.db import connection


import re

# Create your views here.

def show_main(request):
    if request.COOKIES.get('role') is not None:
        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, 'landing.html')
    
def register(request):
    return render(request, 'register.html')
        
def register_atlet(request):
    # if request method post, case 
    if (request.method == 'POST' or request.method == 'post') and not request.method == 'GET':
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        negara = request.POST.get('negara')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        play = request.POST.get('play')
        tinggi_badan = request.POST.get('tinggi_badan')
        jenis_kelamin = request.POST.get('jenis_kelamin')

        if nama == '' or email == '' or negara == '' or tanggal_lahir == '' or play == '' or tinggi_badan == '' or jenis_kelamin == '':
            context = {
                'msg': 'Semua field harus diisi'
            }
            return render(request, 'register-atlet.html', context)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            context = {
                'msg': 'Format email tidak valid'
            }
            return render(request, 'register-atlet.html', context)
        if not re.match(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", tanggal_lahir):
            context = {
                'msg': 'Format tanggal lahir tidak valid. Gunakan format YYYY-MM-DD'
            }
            return render(request, 'register-atlet.html', context)
        if not re.match(r"[0-9]{3}", tinggi_badan):
            context = {
                'msg': 'Format tinggi badan tidak valid. Gunakan format XXX cm'
            }
            return render(request, 'register-atlet.html', context)

    return render(request, 'register-atlet.html')
def register_umpire(request):
    return render(request, 'register-umpire.html')
def register_pelatih(request):
    return render(request, 'register-pelatih.html')

def login(request):
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
            response = HttpResponseRedirect(reverse('home'))
            if is_pelatih != []:
                response.set_cookie('role','pelatih')
            elif is_umpire != []:
                response.set_cookie('role','umpire')
            elif is_atlet != []:
                response.set_cookie('role','atlet')
            response.set_cookie('id', result[0][0])
            response.set_cookie('nama', result[0][1])
            response.set_cookie('email', result[0][2])
            return response
        
        else:
            context = {
                'msg': result
            }
            return render(request, 'login.html', context)
        
        # with connection.cursor() as cursor:

        #     cursor.execute(f'SELECT * FROM babadu.member WHERE nama = \'{nama}\' AND email = \'{email}\';')
        #     global user
        #     user = cursor.fetchone()
        #     if(user is None):
        #         return render(request, 'login.html')
        #     else:
        #         cursor.execute(f'SELECT * FROM babadu.pelatih WHERE id = \'{user[0]}\';')
        #         is_pelatih = cursor.fetchone()

        #         cursor.execute(f'SELECT * FROM babadu.umpire WHERE id = \'{user[0]}\';')
        #         is_umpire = cursor.fetchone()

        #         cursor.execute(f'SELECT * FROM babadu.atlet WHERE id = \'{user[0]}\';')
        #         is_atlet = cursor.fetchone()

        
        #         response = HttpResponseRedirect(reverse('home')) 

        #         if is_pelatih is not None:
        #             response.set_cookie('role','pelatih')
        #             print(1)
        #         elif is_umpire is not None:
        #             response.set_cookie('role','umpire')
        #             print(2)
        #         elif is_atlet is not None:
        #             response.set_cookie('role','atlet')
        #             print(3)
        #         response.set_cookie('id', user[0])
        #         response.set_cookie('nama', user[1])
        #         response.set_cookie('email', user[2])
                
        #         return response
    return render(request, 'login.html')

def logout(request):
    response = HttpResponseRedirect(reverse('show_main'))
    for cookie in request.COOKIES:
        response.delete_cookie(cookie)
    return response

def home(request ):
    if request.COOKIES.get('role') is None:
        return HttpResponseRedirect(reverse('show_main'))
    # get cookie
    print(request.COOKIES.get('role'))
    role = request.COOKIES.get('role')
    id = request.COOKIES.get('id')
    nama = request.COOKIES.get('nama')
    email = request.COOKIES.get('email')

    #  add data to context
    context = {
        'role': role,
        'id': id,
        'nama': nama,
        'email': email,
    }
    return render(request, 'home.html',context)