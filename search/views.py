from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from resources.models import Buku, Kategori, Pengarang, Journal, Kategori_Journal

def search(request):
    search = request.GET.get('q')
    books = Buku.objects.all()
    categories = Kategori.objects.all()

    if search:
        books = books.filter(
            Q(jdl_buku__icontains=search)|Q(kategori__nama_kategori__icontains=search)|Q(pengarang__nama_pengarang__icontains=search)
        )

    
    
    context = {
        "subjudul":"Pencarian",
        "buku": books,
        "cat":categories,
        "search": search,
    }
    
    return render(request, 'resources/kategori.html', context)

def searchj(request):
    searchj = request.GET.get('j')
    journals = Journal.objects.all()
    categoriesj = Kategori_Journal.objects.all()

    if searchj:
        journals = journals.filter(
            Q(jdl_jurnal__icontains=searchj)|Q(kategorij__nama_kategori__icontains=searchj)
        )

    
    
    context = {
        "subjudul":"Pencarian",
        "journals": journals,
        "catj":categoriesj,
        "searchj": searchj,
    }
    
    return render(request, 'resources/kategori_jurnal.html', context)
