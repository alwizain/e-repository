from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from resources.models import Buku, Kategori
from .cart import Cart

def cart_add(request, bukuid):
	cart = Cart(request)  
	buku = get_object_or_404(Buku, id_buku=bukuid) 
	cart.add(buku=buku)

	return redirect('index')

def cart_update(request, bukuid, jumlah):
	cart = Cart(request) 
	buku = get_object_or_404(Buku, id_buku=bukuid) 
	cart.update(buku=buku, jumlah=jumlah)
	harga = (buku.harga*jumlah)

	return render(request, 'cart/price.html', {"harga":harga})

def cart_remove(request, bukuid):
    cart = Cart(request)
    buku = get_object_or_404(Buku, id_buku=bukuid)
    cart.remove(buku)
    return redirect('cart:cart_details')

def total_cart(request):
	return render(request, 'cart/totalcart.html')

def cart_summary(request):

	return render(request, 'cart/summary.html')

def cart_details(request):
	cart = Cart(request)
	context = {
		"cart": cart,
        'judul' : 'Keranjang',
		'subjudul' : "Keranjang",
		'nav' : [
			['nav-link','/', 'Home'],
			['nav-link active', '/resources', 'Resources'],
			['nav-link', '/panduan', 'Panduan'],
			['nav-link', '/dokumen', 'Dokumen'],
			['nav-link','/bantuan', 'Bantuan'],
		]
	}
	return render(request, 'cart/cart.html', context)

