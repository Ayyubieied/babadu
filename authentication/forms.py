from django import forms

class registerFormAtlet(forms.form):
    nama = forms.CharField(label='Nama', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nama', 'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')", 'oninput': "setCustomValidity('')"}))
    email = forms.EmailField(label='Email', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email', 'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')", 'oninput': "setCustomValidity('')"}))
    negara = forms.CharField(label='Negara', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Negara', 'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')", 'oninput': "setCustomValidity('')"}))
    tanggal_lahir = forms.CharField(label='Tanggal Lahir', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Tanggal Lahir', 'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')", 'oninput': "setCustomValidity('')"}))
    # make a input form play, which is a radio button
    play = forms.ChoiceField(label='Play', choices=[('left', 'left'), ('right', 'right')], widget=forms.RadioSelect(  
        attrs={'class': 'form-control', 'placeholder': 'Play', 'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')", 'oninput': "setCustomValidity('')"}))
    tinggi_badan = forms.CharField(label='Tinggi Badan', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Tinggi Badan', 'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')", 'oninput': "setCustomValidity('')"}))
    jenis_kelamin = forms.ChoiceField(label='Jenis Kelamin', choices=[('L', 'L'), ('P', 'P')], widget=forms.RadioSelect(   
        attrs={'class': 'form-control', 'placeholder': 'Jenis Kelamin', 'oninvalid': "this.setCustomValidity('Data yang diisikan belum lengkap, silahkan lengkapi data terlebih dahulu')", 'oninput': "setCustomValidity('')"}))




