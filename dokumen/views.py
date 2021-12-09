from django.shortcuts import render
from django.http import HttpResponse
from .models import Dokumen

# Create your views here.
def index(request):
	data_dokumen = Dokumen.objects.all()

	context = {
		'judul' : 'Dokumen',
		'subjudul' : "Dokumen",
		# 'logo':'img/logo_nav.png',
		'data_dokumen':data_dokumen,
		'nav' : [
			['nav-link','/', 'Home'],
			['nav-link', '/resources', 'Resources'],
			['nav-link', '/panduan', 'Panduan'],
			['nav-link active', '/dokumen', 'Dokumen'],
			['nav-link','/bantuan', 'Bantuan'],
		]
	}
	return render(request,'dokumen/index.html',context)

def download(request,path):
	file_path=os.path.join(settings.MEDIA_ROOT,path)
	if os.path.exists(file_path):
		with open(file_path,'rt')as fl:
			response=HttpResponse(fl.read(),content_type="application/file")
			response['Content-Disposition']='inline;filename='+os.path.basename(file_path)
			return response

	raise Http404
