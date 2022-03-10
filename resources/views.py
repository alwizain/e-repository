from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from resources.helpers import genre_wise, tfidf_recommendations, get_book_dict, get_rated_bookids, combine_ids, embedding_recommendations, get_top_n, popular_among_users
from .models import Journal, Buku, Kategori, Kategori_Journal, Pengarang, Review, UserRating
import repository.settings as settings
from django.contrib import messages
from repository.forms import ReviewForm, RatingForm

import random
import operator

import pandas as pd
import os
import json
import requests

'''
    Production File Path :  staticfiles_storage.url(file)
    Developement File Path : settings.STATICFILES_DIRS[0] + 'app/.../file'
'''
book_path = os.path.join(settings.STATICFILES_DIRS[0] + '/dataset/books.csv')

# import codecs
# from math import sqrt

# from django.db.models import Q
# from django.db.models import Case, When
# from .recommendation import update_clusters
# import numpy as np
# import pandas as pd

# from mainapp.helpers import tfidf_recommendations, get_book_dict, get_rated_bookids, combine_ids, embedding_recommendations
# from mainapp.models import UserRating

# Create your views here.
      
def index(request):
    bukubaru = Buku.objects.order_by('-created')[:5]
    jurnalbaru = Journal.objects.order_by('-created')[:5]
    bukubaik = Buku.objects.order_by('-totalrating')[:4]
    books = popular_among_users()

    # df = pd.DataFrame(list(Review.objects.all().values()))
    # # # if new user not rated any movie
    # # if user_name > nu:
    # #     product = Product.objects.get(id=15)
    # #     q = Review(user=request.user, product=product, rating=0)
    # #     q.save()

    # print("Current user id: ")
    # prediction_matrix, Ymean = Myrecommend()
    # my_predictions = prediction_matrix[:, ] + Ymean.flatten()
    # pred_idxs_sorted = np.argsort(my_predictions)
    # pred_idxs_sorted[:] = pred_idxs_sorted[::-1]
    # pred_idxs_sorted = pred_idxs_sorted + 1
    # print(pred_idxs_sorted)
    # preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pred_idxs_sorted)])
    # movie_list = list(Buku.objects.filter(id__in=pred_idxs_sorted, ).order_by(preserved)[:10])
    context = {
		'judul' : 'Resources',
		'subjudul' : "Resources",
		# 'logo':'img/logo_nav.png',
        'newbooks' : bukubaru,
        'newjournal' : jurnalbaru,
        'ratingbuku' : bukubaik,
        # 'movie_list': movie_list,
        'books': books,
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
		'subjudul' : 'Jurnal',
		'jurnal':data_journal,
		'kategori':data_kategori,
		'nav' : [
			['nav-link','/', 'Home'],
			['nav-link', '/resources', 'Resources'],
			['nav-link', '/panduan', 'Panduan'],
			['nav-link', '/dokumen', 'Dokumen'],
			['nav-link','/bantuan', 'Bantuan'],
		]
	}
	return render(request, 'resources/jurnal.html', context)

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
        'subjudul' : "Jurnal",
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
    categories = Kategori.objects.all()
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
        'cat' : categories,
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
    paginator = Paginator(bukus_, 20)
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
    paginator = Paginator(buku_, 20)
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

def get_rbuku(request, bookid):
    df_book = pd.read_csv(book_path)
    book_details = df_book[df_book['book_id'] == bookid]
    bukulain = popular_among_users(N=50)
    form = RatingForm(request.POST or None)
    r_review = UserRating.objects.filter(bookid=bookid)
    if request.user.is_authenticated:
        user_ratings = list(UserRating.objects.filter(user=request.user).order_by('-bookrating'))
        random.shuffle(user_ratings)
        best_user_ratings = sorted(user_ratings, key=operator.attrgetter('bookrating'), reverse=True)

        if len(best_user_ratings) < 4:
            messages.info(request, 'Please rate atleast 5 books')
            return redirect('index')
        if best_user_ratings:
            # If one or more book is rated
            bookid = best_user_ratings[0].bookid
            already_rated_books = get_rated_bookids(user_ratings)
            # Get bookids based on TF-IDF weighing
            tfidf_bookids = set(tfidf_recommendations(bookid))

            # Shuffle again for randomness for second approach
            random.shuffle(user_ratings)
            best_user_ratings = sorted(user_ratings, key=operator.attrgetter('bookrating'), reverse=True)
            # Get Top 10 bookids based on embedding
            embedding_bookids = set(embedding_recommendations(best_user_ratings))

            best_bookids = combine_ids(tfidf_bookids, embedding_bookids, already_rated_books)
            all_books_dict = get_book_dict(best_bookids)
        else:
            return redirect('index')
        context = {
            'judul' : 'Buku',
            'subjudul' : "Buku",
            'buku': book_details,
            'books': all_books_dict,
            'rekombuku': bukulain,
            'nav' : [
                ['nav-link','/', 'Home'],
                ['nav-link', '/resources', 'Resources'],
                ['nav-link', '/panduan', 'Panduan'],
                ['nav-link', '/dokumen', 'Dokumen'],
                ['nav-link','/bantuan', 'Bantuan'],
            ]
        }
        return render(request, "resources/read.html", context)
    else:
        paginator = Paginator(r_review, 4)
        page = request.GET.get('page')
        rreview = paginator.get_page(page)

        if request.method == 'POST':
            if request.user.is_authenticated:
                if form.is_valid():
                    temp = form.save(commit=False) 
                    temp.user = User.objects.get(id=request.user.id)
                    temp.bookid = bookid             
                    temp = df_book[df_book['book_id'] == bookid]
                    temp.totalreview += 1
                    temp.totalrating += int(request.POST.get('bookrating'))
                    form.save()  
                    temp.save()

                    messages.success(request, "Review Added Successfully")
                    form = RatingForm()
            else:
                messages.error(request, "You need login first.")

        context = {
            'judul' : 'Buku',
            'subjudul' : "Buku",
            'buku': book_details,
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
        return render(request, "resources/read.html", context)

def get_rbooks(request):
    '''
        View to Render Explore Page
        Renders Top N Books
    '''
    N = 152
    sample = get_top_n().sample(N).to_dict('records')
    paginator = Paginator(sample, 40)
    page = request.GET.get('page')
    rbukus = paginator.get_page(page)
    context = {
        'subjudul' : "Buku",
        'rbuku': rbukus,
        'nav' : [
			['nav-link','/', 'Home'],
			['nav-link', '/resources', 'Resources'],
			['nav-link', '/panduan', 'Panduan'],
			['nav-link', '/dokumen', 'Dokumen'],
			['nav-link','/bantuan', 'Bantuan'],
		]
    }
    return render(request, 'resources/rkategori.html', context)

def get_genre_books(request, genre):
    '''
        View to render Books in a particular genre
    '''
    genre_topbooks = genre_wise(genre)
    genre_topbooks = genre_topbooks.to_dict('records')
    paginator = Paginator(genre_topbooks, 10)
    page = request.GET.get('page')
    rbukus = paginator.get_page(page)
    context = {
        'subjudul' : "Buku",
        'rbuku': rbukus,
        'nav' : [
			['nav-link','/', 'Home'],
			['nav-link', '/resources', 'Resources'],
			['nav-link', '/panduan', 'Panduan'],
			['nav-link', '/dokumen', 'Dokumen'],
			['nav-link','/bantuan', 'Bantuan'],
		]
    }
    return render(request, 'resources/rkategori.html', context)

def book_recommendations(request):
    '''
        View to render book recommendations

        Count Vectorizer Approach:
            1. Get Ratings of User
            2. Shuffle by Top Ratings(For Randomness each time)
            3. Recommend according to Top Rated Book
    '''
    user_ratings = list(UserRating.objects.filter(user=request.user).order_by('-bookrating'))
    random.shuffle(user_ratings)
    best_user_ratings = sorted(user_ratings, key=operator.attrgetter('bookrating'), reverse=True)

    if len(best_user_ratings) < 4:
        messages.info(request, 'Please rate atleast 5 books')
        return redirect('index')
    if best_user_ratings:
        # If one or more book is rated
        bookid = best_user_ratings[0].bookid
        already_rated_books = get_rated_bookids(user_ratings)
        # Get bookids based on TF-IDF weighing
        tfidf_bookids = set(tfidf_recommendations(bookid))

        # Shuffle again for randomness for second approach
        random.shuffle(user_ratings)
        best_user_ratings = sorted(user_ratings, key=operator.attrgetter('bookrating'), reverse=True)
        # Get Top 10 bookids based on embedding
        embedding_bookids = set(embedding_recommendations(best_user_ratings))

        best_bookids = combine_ids(tfidf_bookids, embedding_bookids, already_rated_books)
        all_books_dict = get_book_dict(best_bookids)
    else:
        return redirect('index')

    context = {
        'subjudul' : "Rekomendasi Buku",
        'books': all_books_dict,
        'nav' : [
			['nav-link','/', 'Home'],
			['nav-link', '/resources', 'Resources'],
			['nav-link', '/panduan', 'Panduan'],
			['nav-link', '/dokumen', 'Dokumen'],
			['nav-link','/bantuan', 'Bantuan'],
		]
    }
    return render(request, 'resources/recommendation.html', context)



# def recommend(request):
#     df = pd.DataFrame(list(Review.objects.all().values()))
#     nu = df.reviewer.unique().shape[0]
#     current_user_id = request.reviewer_id
#     # # if new user not rated any movie
#     # if user_name > nu:
#     #     product = Product.objects.get(id=15)
#     #     q = Review(user=request.user, product=product, rating=0)
#     #     q.save()

#     print("Current user id: ", current_user_id)
#     prediction_matrix, Ymean = Myrecommend()
#     my_predictions = prediction_matrix[:, current_user_id - 1] + Ymean.flatten()
#     pred_idxs_sorted = np.argsort(my_predictions)
#     pred_idxs_sorted[:] = pred_idxs_sorted[::-1]
#     pred_idxs_sorted = pred_idxs_sorted + 1
#     print(pred_idxs_sorted)
#     preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pred_idxs_sorted)])
#     movie_list = list(Buku.objects.filter(id__in=pred_idxs_sorted, ).order_by(preserved)[:10])
#     return render(request, 'resources/index.html', {'movie_list': movie_list})


