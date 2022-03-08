from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    context = {
		'judul' : 'Berita',
		'subjudul' : "Berita",
		# 'logo':'img/logo_nav.png',
		'nav' : [
			['nav-link','/', 'Home'],
			['nav-link', '/resources', 'Resources'],
			['nav-link ', '/panduan', 'Panduan'],
			['nav-link', '/dokumen', 'Dokumen'],
			['nav-link active','/bantuan', 'Bantuan'],
		]
	}
    return render(request,'berita/index.html',context)

def detailberita(request, id):
    context = {
		'judul' : 'Berita',
		'subjudul' : "Berita",
		'id' : id,
		# 'logo':'img/logo_nav.png',
		'nav' : [
			['nav-link','/', 'Home'],
			['nav-link', '/resources', 'Resources'],
			['nav-link ', '/panduan', 'Panduan'],
			['nav-link', '/dokumen', 'Dokumen'],
			['nav-link active','/bantuan', 'Bantuan'],
		]
	}
    return render(request,'berita/detailberita.html',context)