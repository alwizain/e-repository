from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Journal, Buku, Kategori, Pengarang, Review
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from .forms import RegistrationForm, ReviewForm

# Create your views here.
def index(request):
	
	context = {
		'judul' : 'Resources',
		'subjudul' : "Resources",
		# 'logo':'img/logo_nav.png',
		'nav' : [
			['nav-link','/', 'Home'],
			['nav-link active', '/resources', 'Resources'],
			['nav-link', '/panduan', 'Panduan'],
			['nav-link', '/dokumen', 'Dokumen'],
			['nav-link','/bantuan', 'Bantuan'],
            ['nav-link','/resources/jurnal', 'Journal'],
		]
	}
	return render(request,'resources/index.html',context)

def get_journal(request):
	data_journal = Journal.objects.all()
	data_kategori = Kategori.objects.all()
	context = {
		'judul' : 'Journal',
		'subjudul' : "Journal",
		# 'logo':'img/logo_nav.png',
		'journal':data_journal,
		'kategori':data_kategori,
		'nav' : [
			['nav-link','/', 'Home'],
			['nav-link', '/resources', 'Resources'],
			['nav-link', '/panduan', 'Panduan'],
			['nav-link', '/dokumen', 'Dokumen'],
			['nav-link','/bantuan', 'Bantuan'],
            ['nav-link active','/resources/jurnal', 'Journal'],
		]
	}
	return render(request,'resources/jurnal.html',context)

def download(request,path):
	file_path=os.path.join(settings.MEDIA_ROOT,path)
	if os.path.exists(file_path):
		with open(file_path,'rt')as fl:
			response=HttpResponse(fl.read(),content_type="application/file")
			response['Content-Disposition']='inline;filename='+os.path.basename(file_path)
			return response

	raise Http404
