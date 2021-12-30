from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm

# #method view
def index(request):
	context = {
		'judul' : 'Home',
		'subjudul' : "Selamat Datang",
		'deskripsi' : "Perpustakaan Digital Masa Kini",
		# 'logo':'img/logo_nav.png',
		# 'logo_sml':'img/logo_sml.png',
		'nav' : [
			['nav-link active','/', 'Home'],
			['nav-link dropdown-toggle', '/resources', 'Resources'],
			['dropdown-item', '/panduan', 'Panduan'],
			['nav-link', '/panduan', 'Panduan'],
			['nav-link', '/dokumen', 'Dokumen'],
			['nav-link','/bantuan', 'Bantuan'],
		]
	}

	return render(request,'index.html',context)

def signin(request):
    if request.user.is_authenticated:
        return redirect('indexuser')
    else:
        if request.method == "POST":
            user = request.POST.get('user')
            password = request.POST.get('pass')
            auth = authenticate(request, username=user, password=password)
            if auth is not None:
                login(request, auth)
                return redirect('indexuser')
            else:
            	messages.error(request, 'username and password doesn\'t match')

    return render(request, "login.html")

def signout(request):
    logout(request)
    return redirect('indexuser')	


def registration(request):
	form = RegistrationForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('signin')

	return render(request, 'signup.html', {"form": form})