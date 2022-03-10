from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
	path('buku/', views.search, name='search'),
	path('jurnal/', views.searchj, name='searchj'),
]
