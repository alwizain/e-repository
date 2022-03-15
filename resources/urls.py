from django.urls import path 
from .import views, views_ajax
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.static import serve


urlpatterns = [
	path('', views.index, name='index'),
    path('detail_jurnal/<int:id>', views.get_journal, name="journal"),
	path('jurnal', views.get_journals, name="journals"),
	path('kategori_jurnal/<int:id>', views.get_journal_kategori, name="kategorij"),
	url('download/(?P<path>.*)',serve,{'document_root':settings.MEDIA_ROOT}),
	path('buku/<int:id>', views.get_buku, name="buku"),
	path('kategori_buku', views.get_bukus, name="bukus"),
	path('kategori_buku/<int:id>', views.get_buku_kategori, name="kategori"),
	path('penulis/<int:id>', views.get_pengarang, name = "pengarang"),
	path('rbuku/<int:bookid>', views.get_rbuku, name="rbuku"),
	path('rbooks/', views.get_rbooks, name="rbooks"),
	path('rkategori/<genre>', views.get_genre_books, name="rkategori"),
	path('recommendations/', views.book_recommendations, name='book_recommendations'),
	path('recommen/', views.recommendations, name='recommendations'),

]
if settings.DEBUG:
	urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
	urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# Ajax Views
urlpatterns += [
    path('search_ajax/', views_ajax.search, name='search_ajax'),
    path('book_summary_ajax/', views_ajax.book_summary, name='summary_ajax'),
    path('book_details_ajax/', views_ajax.get_book_details, name='book_details'),
    path('user_rate_book/', views_ajax.user_rate_book, name='user_rate_book'),
    path('save_book/', views_ajax.save_book, name='save_book'),
    path('remove_saved_book/', views_ajax.remove_saved_book, name='remove_saved_book')
]
