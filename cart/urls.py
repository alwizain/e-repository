from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
	path('', views.cart_details, name='cart_details'),
	path('summary', views.cart_summary, name='cart_summary'),
	path('totalcart', views.total_cart, name='totalcart'),
	path('add/<int:bukuid>', views.cart_add, name='cart_add'),
	path('remove/<int:bukuid>', views.cart_remove, name='cart_remove'),
	path('update/<int:bukuid>/<int:jumlah>', views.cart_update, name='cart_update'),
]
