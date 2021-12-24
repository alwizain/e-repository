from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import Journal, Buku, Kategori, Kategori_Journal, Pengarang, Review
from django.contrib import messages
from repository.forms import ReviewForm

# Create your views here.
def index(request):
    bukubaru = Buku.objects.order_by('-created')[:5]
    jurnalbaru = Journal.objects.order_by('-created')[:5]
    bukubaik = Buku.objects.order_by('-totalrating')[:4]
    context = {
		'judul' : 'Resources',
		'subjudul' : "Resources",
		# 'logo':'img/logo_nav.png',
        'newbooks' : bukubaru,
        'newjournal' : jurnalbaru,
        'ratingbuku' : bukubaik,
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

def get_journal(request, id):
	data_journal = get_object_or_404(Journal, kd_jurnal=id)
	data_kategori = Kategori_Journal.objects.all()

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
    journals_ = Journal.objects.all().order_by('-created')
    data_kategori = Kategori_Journal.objects.all()
    
    context = {
		'judul' : 'Journal',
		'subjudul' : "Journal",
		# 'logo':'img/logo_nav.png',
		'journals':journals_,
		'catj':data_kategori,
		'nav' : [
			['nav-link','/', 'Home'],
			['nav-link', '/resources', 'Resources'],
			['nav-link', '/panduan', 'Panduan'],
			['nav-link', '/dokumen', 'Dokumen'],
			['nav-link','/bantuan', 'Bantuan'],
		]
	}
    return render(request, "resources/kategori_jurnal.html", context)

def get_journal_kategori(request, id):
    journal_ = Journal.objects.filter(kategorij_id=id)
    paginator = Paginator(journal_, 10)
    page = request.GET.get('page')
    journal = paginator.get_page(page)
    categories = Kategori_Journal.objects.all()
    context = {
        'subjudul' : "Journal",
        'journals' : journal,
		"catj":categories,
        'nav' : [
			['nav-link','/', 'Home'],
			['nav-link', '/resources', 'Resources'],
			['nav-link', '/panduan', 'Panduan'],
			['nav-link', '/dokumen', 'Dokumen'],
			['nav-link','/bantuan', 'Bantuan'],
		]
    }
    return render(request, "resources/kategori_jurnal.html", context)

def get_buku(request, id):
    bukulain = Buku.objects.order_by('-created')[:8]
    form = ReviewForm(request.POST or None)
    buku = get_object_or_404(Buku, id_buku=id)
    rbukus = Buku.objects.filter(kategori_id=buku.kategori.id_kategori)
    r_review = Review.objects.filter(buku_id=id).order_by('-created')

    paginator = Paginator(r_review, 4)
    page = request.GET.get('page')
    rreview = paginator.get_page(page)

    if request.method == 'POST':
        if request.user.is_authenticated:
            if form.is_valid():
                temp = form.save(commit=False)
                temp.reviewer = User.objects.get(id=request.user.id)
                temp.buku = buku          
                temp = Buku.objects.get(id_buku=id)
                temp.totalreview += 1
                temp.totalrating += int(request.POST.get('review_star'))
                form.save()  
                temp.save()

                messages.success(request, "Review Added Successfully")
                form = ReviewForm()
        else:
            messages.error(request, "You need login first.")
    context = {
        'judul' : 'Buku',
        'subjudul' : "Buku",
        'buku':buku,
        'rbukus': rbukus,
        'rekombuku': bukulain,
        'form': form,
        'rreview': rreview,
        'nav' : [
			['nav-link','/', 'Home'],
			['nav-link', '/resources', 'Resources'],
			['nav-link', '/panduan', 'Panduan'],
			['nav-link', '/dokumen', 'Dokumen'],
			['nav-link','/bantuan', 'Bantuan'],
		]
    }
    return render(request, 'resources/buku.html', context)


def get_bukus(request):
    bukus_ = Buku.objects.all().order_by('-created')
    paginator = Paginator(bukus_, 10)
    page = request.GET.get('page')
    bukus = paginator.get_page(page)
    categories = Kategori.objects.all()
    context = {
        'subjudul' : "Buku",
        "buku":bukus,
		"cat":categories,
        'nav' : [
			['nav-link','/', 'Home'],
			['nav-link', '/resources', 'Resources'],
			['nav-link', '/panduan', 'Panduan'],
			['nav-link', '/dokumen', 'Dokumen'],
			['nav-link','/bantuan', 'Bantuan'],
		]
    }
    return render(request, "resources/kategori.html", context)

def get_buku_kategori(request, id):
    buku_ = Buku.objects.filter(kategori_id=id)
    paginator = Paginator(buku_, 10)
    page = request.GET.get('page')
    buku = paginator.get_page(page)
    categories = Kategori.objects.all()
    context = {
        'subjudul' : "Buku",
        "buku":buku,
		"cat":categories,
        'nav' : [
			['nav-link','/', 'Home'],
			['nav-link', '/resources', 'Resources'],
			['nav-link', '/panduan', 'Panduan'],
			['nav-link', '/dokumen', 'Dokumen'],
			['nav-link','/bantuan', 'Bantuan'],
		]
    }
    return render(request, "resources/kategori.html", context)

def get_pengarang(request, id):
    wrt = get_object_or_404(Pengarang, id_pengarang=id)
    buku = Buku.objects.filter(pengarang_id=wrt.id_pengarang)
    context = {
        'subjudul' : "Penulis",
        "wrt": wrt,
        "buku": buku,
        'nav' : [
			['nav-link','/', 'Home'],
			['nav-link', '/resources', 'Resources'],
			['nav-link', '/panduan', 'Panduan'],
			['nav-link', '/dokumen', 'Dokumen'],
			['nav-link','/bantuan', 'Bantuan'],
		]
    }
    return render(request, "resources/penulis.html", context)


