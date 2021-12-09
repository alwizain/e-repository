from django.shortcuts import render
from django.http import HttpResponse
# from .models import Rp_Journal dipakai
from rest_framework import viewsets
from rest_framework import permissions
# from journal.serializers import JournalSerializer dipakai

# Create your views here.
def index(request):
	# data_journal = Rp_Journal.objects.all()

	context = {
		'judul' : 'Journal',
		'subjudul' : "Journal",
		# 'logo':'img/logo_nav.png',
		# 'journal':data_journal,
		'nav' : [
			['nav-link','/', 'Home'],
			['nav-link', '/resources', 'Resources'],
			['nav-link', '/panduan', 'Panduan'],
			['nav-link', '/dokumen', 'Dokumen'],
			['nav-link','/bantuan', 'Bantuan'],
		]
	}
	return render(request,'journal/index.html',context)

def download(request,path):
	file_path=os.path.join(settings.MEDIA_ROOT,path)
	if os.path.exists(file_path):
		with open(file_path,'rt')as fl:
			response=HttpResponse(fl.read(),content_type="application/file")
			response['Content-Disposition']='inline;filename='+os.path.basename(file_path)
			return response

	raise Http404

# class JournalViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = Rp_Journal.objects.all().order_by('-kd_jurnal')
#     serializer_class = JournalSerializer
#     permission_classes = [permissions.IsAuthenticated]