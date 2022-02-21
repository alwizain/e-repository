from django.urls import path 
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.static import serve

urlpatterns = [
	path('', views.index, name='index'),
    path('journal/<int:id>', views.get_journal, name="journal"),
	path('journals', views.get_journals, name="journals"),
	path('kategorij/<int:id>', views.get_journal_kategori, name="kategorij"),
	url('download/(?P<path>.*)',serve,{'document_root':settings.MEDIA_ROOT}),
	path('buku/<int:id>', views.get_buku, name="buku"),
	path('bukus', views.get_bukus, name="bukus"),
	path('kategori/<int:id>', views.get_buku_kategori, name="kategori"),
	path('penulis/<int:id>', views.get_pengarang, name = "pengarang"),
	path('rbuku/<int:bookid>', views.get_rbuku, name="rbuku"),
	path('rbooks/', views.get_rbooks, name="rbooks"),
	path('rkategori/<genre>', views.get_genre_books, name="rkategori"),
	path('recommendations/', views.book_recommendations, name='book_recommendations'),
]

if settings.DEBUG:
	urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
	urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)