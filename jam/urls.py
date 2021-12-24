from django.urls import path 
from jam import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.static import serve

urlpatterns = [
	path('', views.index, name='jam'),
]

if settings.DEBUG:
	urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
	urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)