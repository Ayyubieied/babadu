from django import forms
from utils.query import *

class UjianKualifikasiForm(forms.Form):
    tahun = forms.CharField(label='Tahun', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Tahun', 'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')", 'oninput': "setCustomValidity('')"}))
    batch = forms.CharField(label='Batch', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Batch', 'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')", 'oninput': "setCustomValidity('')"}))
    tempat_pelaksanaan = forms.CharField(label='Tempat Pelaksanaan', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Tempat Pelaksanaan', 'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')", 'oninput': "setCustomValidity('')"}))
    tanggal_pelaksanaan = forms.DateField(label='Tanggal Pelaksanaan', widget=forms.DateInput(
        attrs={'class': 'form-control', 'placeholder': 'Tanggal Pelaksanaan', 'type': 'date'}))
    