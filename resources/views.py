from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import Journal, Buku, Kategori, Pengarang, Review
from django.contrib import messages
from repository.forms import ReviewForm

# Create your views here.
def index(request):
    bukubaru = Buku.objects.order_by('-created')[:5]
    jurnalbaru = Journal.objects.order_by('-created')[:5]
    context = {
		'judul' : 'Resources',
		'subjudul' : "Resources",
		# 'logo':'img/logo_nav.png',
        'newbooks' : bukubaru,
        'newjournal' : jurnalbaru,
		'nav' : [
			['nav-link','/', 'Home'],
			['nav-link active', '/resources', 'Resources'],
			['nav-link', '/panduan', 'Panduan'],
			['nav-link', '/dokumen', 'Dokumen'],
			['nav-link','/bantuan', 'Bantuan'],
		]
	}
    return render(request,'resources/index.html',context)

def download(request,path):
	file_path=os.path.join(settings.MEDIA_ROOT,path)
	if os.path.exists(file_path):
		with open(file_path,'rt')as fl:
			response=HttpResponse(fl.read(),content_type="application/file")
			response['Content-Disposition']='inline;filename='+os.path.basename(file_path)
			return response

	raise Http404

def get_journal(request, kd_jurnal):
	data_journal = get_object_or_404(Journal, id=kd_jurnal)
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
		]
	}
	return render(request, "resources/jurnal.html", context)

def get_journals(request):
    journals_ = Journal.objects.all()
    data_kategori = Kategori.objects.all()
    
    context = {
		'judul' : 'Journal',
		'subjudul' : "Journal",
		# 'logo':'img/logo_nav.png',
		'journals':journals_,
		'kategori':data_kategori,
		'nav' : [
			['nav-link','/', 'Home'],
			['nav-link', '/resources', 'Resources'],
			['nav-link', '/panduan', 'Panduan'],
			['nav-link', '/dokumen', 'Dokumen'],
			['nav-link','/bantuan', 'Bantuan'],
		]
	}
    return render(request, "resources/jurnal.html", context)

def get_buku(request, id_buku):
    form = ReviewForm(request.POST or None)
    buku = get_object_or_404(Buku, id=id_buku)
    rbukus = Buku.objects.filter(id_kategori=buku.kategori.id)
    r_review = Review.objects.filter(id=id_buku).order_by('-created')

    paginator = Paginator(r_review, 4)
    page = request.GET.get('page')
    rreview = paginator.get_page(page)

    if request.method == 'POST':
        if request.user.is_authenticated:
            if form.is_valid():
                temp = form.save(commit=False)
                temp.customer = User.objects.get(id=request.user.id)
                temp.buku = buku          
                temp = Buku.objects.get(id=id_buku)
                temp.totalreview += 1
                temp.totalrating += int(request.POST.get('review_star'))
                form.save()  
                temp.save()

                messages.success(request, "Review Added Successfully")
                form = ReviewForm()
        else:
            messages.error(request, "You need login first.")
    context = {
        'buku':buku,
        'rbukus': rbukus,
        'form': form,
        'rreview': rreview
    }
    return render(request, 'resources/buku.html', context)


def get_bukus(request):
    bukus_ = Buku.objects.all().order_by('-created')
    paginator = Paginator(bukus_, 10)
    page = request.GET.get('page')
    bukus = paginator.get_page(page)
    return render(request, "resources/kategori.html", {"buku":bukus})

def get_buku_kategori(request, id):
    buku_ = Buku.objects.filter(id_kategori=id)
    paginator = Paginator(buku_, 10)
    page = request.GET.get('page')
    buku = paginator.get_page(page)
    return render(request, "resources/kategori.html", {"buku":buku})

def get_pengarang(request, id_pengarang):
    wrt = get_object_or_404(Pengarang, id=id_pengarang)
    buku = Buku.objects.filter(pengarang_id=wrt.id)
    context = {
        "wrt": wrt,
        "buku": buku
    }
    return render(request, "resources/penulis.html", context)


