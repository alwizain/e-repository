from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    context = {
		'judul' : 'Panduan',
		'subjudul' : "Panduan",
		# 'logo':'img/logo_nav.png',
		'nav' : [
			['nav-link','/', 'Home'],
			['nav-link', '/resources', 'Resources'],
			['nav-link active', '/panduan', 'Panduan'],
			['nav-link', '/dokumen', 'Dokumen'],
			['nav-link','/bantuan', 'Bantuan'],
		]
	}
    return render(request,'panduan/index.html',context)
