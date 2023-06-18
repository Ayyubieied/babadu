from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from utils.query import *
from django.db import connection
from authentication.forms import *
from authentication.views import *
from ujian_kualifikasi.forms import *
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from datetime import timedelta


import re

def check_ujian(request, tahun, batch, tempat, tanggal):
    id = request.COOKIES.get('id')
    print(tahun)
    print(batch)
    print(tempat)
    print(tanggal)

    # from tanggal above add 1 day and tanggal only without time

    tanggal = datetime.strptime(tanggal, '%Y-%m-%d') + timedelta(days=1)
    tanggal = str(tanggal).split(' ')[0]
    print(tanggal)
    result = execute_query(f'SELECT check_atlet_is_ujian(\'{id}\', {tahun}, {batch}, \'{tempat}\', \'{tanggal}\');')
   
    if result[0][0]:
        result = execute_query(f'SELECT * FROM babadu.ujian_kualifikasi;')
        context = {
            'data_ujian': result,
            'message': 'Anda sudah mengikuti ujian kualifikasi ini'
        }
        response = HttpResponseRedirect(reverse('ujian_kualifikasi:show_ujian'))
        response.set_cookie('error', False)
        return response 
    else:
        print('masuk else')
        response =  HttpResponseRedirect(reverse('ujian_kualifikasi:show_soal'))
        response.set_cookie('tahun', tahun)
        response.set_cookie('batch', batch)
        response.set_cookie('tempat', tempat)
        response.set_cookie('tanggal', tanggal)
        return response
    


def show_ujian(request):
    role_user = request.COOKIES.get('role')
    if role_user is None:
        return HttpResponseRedirect(reverse('authentication:show_main'))
    elif role_user  == 'atlet':
        result = execute_query(f'SELECT * FROM babadu.ujian_kualifikasi;')
        print(result)
        response =  render(request, 'list-ujian-atlet.html', {'data_ujian': result})
        response.delete_cookie('error')
        return response
    elif role_user == 'umpire':
        result = execute_query(f'SELECT * FROM babadu.ujian_kualifikasi;')
        print(result)
        return render(request, 'list-ujian-umpire.html', {'data_ujian': result})
    else:
        return HttpResponseRedirect(reverse('authentication:show_main'))
def create_ujian(request):

    role_user = request.COOKIES.get('role')
    if role_user == 'umpire':
        if (request.method == 'POST'):
            tahun = request.POST.get('tahun')
            batch = request.POST.get('batch')
            tempat_pelaksanaan = request.POST.get('tempat_pelaksanaan')
            tanggal_pelaksanaan = request.POST.get('tanggal_pelaksanaan')
            # check tahun and batch must be integer
            if not (re.match("^[0-9]*$", tahun) and re.match("^[0-9]*$", batch)):
                form = UjianKualifikasiForm(request.POST or None)
                context ={
                    'form': form,
                    'msg': 'Tahun dan Batch harus berupa angka'
                }
                return render(request, 'create-ujian.html', context)
            
            error, result = try_except_query(f'insert into ujian_kualifikasi values({tahun}, {batch}, \'{tempat_pelaksanaan}\', \'{tanggal_pelaksanaan}\');')
            if error:
                form = UjianKualifikasiForm(request.POST or None)
                context ={
                    'form': form,
                    'msg': result
                }
                return render(request, 'create-ujian.html', context)
            else:
                form = UjianKualifikasiForm(request.POST or None)
                context ={
                    'form': form,
                    'success': 'Ujian berhasil dibuat'
                }
                return render(request, 'create-ujian.html', context)
        else:
            form = UjianKualifikasiForm(request.POST or None)
            context ={
                'form': form
            }
            return render(request, 'create-ujian.html', context)
    else:
        # show 404 page
        return HttpResponseRedirect(reverse('authentication:show_main')) 
    
def show_riwayat(requesŧ):
    if requesŧ.COOKIES.get('role') is None:
        return HttpResponseRedirect(reverse('authentication:login'))
    id_user_login = requesŧ.COOKIES.get('id')

    if requesŧ.COOKIES.get('role') == 'umpire':
        result = execute_query(f'SELECT m.nama, a.tahun, a.batch, a.tempat, a.tanggal, a.hasil_lulus FROM member m, atlet_non_kualifikasi_ujian_kualifikasi a where m.id = a.id_atlet;')
        
        return render(requesŧ, 'riwayat-ujian-umpire.html', {'data_ujian': result})

    elif requesŧ.COOKIES.get('role') == 'atlet':    
        
        result = execute_query(f'SELECT * FROM atlet_non_kualifikasi_ujian_kualifikasi where id_atlet=\'{id_user_login}\';')
        print(result)
        return render(requesŧ, 'riwayat-ujian-atlet.html', {'data_ujian': result})
    else:
        return HttpResponseRedirect(reverse('authentication:login'))
    
@csrf_exempt
def show_soal(request):
    if request.COOKIES.get('role') is None:
        return HttpResponseRedirect(reverse('authentication:login'))
    if request.COOKIES.get('role2') == 'atlet-non-kualifikasi':
        if request.method == 'POST':
            score = request.POST.get('score')
            print(score)
            score= int(score)
            tahun = request.COOKIES.get('tahun')
            batch = request.COOKIES.get('batch')
            tempat = request.COOKIES.get('tempat')
            tanggal = request.COOKIES.get('tanggal')
            id_atlet = request.COOKIES.get('id')
            if score>= 4:
                print(tahun, batch, tempat, tanggal, id_atlet)
                error, result = try_except_query(f'select qualifying_atlet(\'{id_atlet}\',{tahun}, {batch}, \'{tempat}\', \'{tanggal}\', true );')
                print(result)
                print("selamat anda lulus")
                context = {
                    'score': score
                }
                return render(request, 'soal-ujian.html', context)

            else:
                print("maaf anda tidak lulus")
                error, result = try_except_query(f'select qualifying_atlet(\'{id_atlet}\',{tahun}, {batch}, \'{tempat}\', \'{tanggal}\', false );')
                context = {
                    'score': score
                }
                return render(request, 'soal-ujian.html',context)


        else:
            print('masuk')
            return render(request, 'soal-ujian.html')
    else:
        return HttpResponseRedirect(reverse('authentication:show_main'))
    
def show_hasil_ujian(request):
    return render(request, 'hasil-ujian.html')