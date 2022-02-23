from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from cart.cart import Cart
from .models import Pembelian, Item_Pembelian
from .forms import OrderCreateForm
from .pdfcreator import renderPdf
import midtransclient



def order_create(request):
	cart = Cart(request)
	if request.user.is_authenticated:
		akun = get_object_or_404(User, id=request.user.id)
		form = OrderCreateForm(request.POST or None, initial={"nama": akun.first_name, "nama_belakang": akun.last_name, "email": akun.email})
		context = {
			'subjudul' : "Checkout",
			'akun' : akun,
			'form' : form,
			# 'logo':'img/logo_nav.png',
			'nav' : [
				['nav-link','/', 'Home'],
				['nav-link', '/resources', 'Resources'],
				['nav-link ', '/panduan', 'Panduan'],
				['nav-link', '/dokumen', 'Dokumen'],
				['nav-link active','/bantuan', 'Bantuan'],
			]
	
		}
  
		if request.method == 'POST':
			if form.is_valid():
				order = form.save(commit=False)
				order.Akun = User.objects.get(id=request.user.id)
				order.payable = cart.get_total_price()
				order.total_buku = len(cart) # len(cart.cart) // number of individual book
				order.save()

				for item in cart:
					Item_Pembelian.objects.create(
						pembelian=order, 
						buku=item['buku'], 
						harga=item['harga'], 
						jumlah=item['jumlah']
						)
				cart.clear()
				
				data = {
					"id_transaksi": order.kd_transaksi,
					"payable": int(order.payable),
					"nama": order.nama,
					"nama_belakang": order.nama_belakang,
					"instansi": order.instansi,
					"email": order.email,
					"telepon": order.telepon
				}
    
				token = midtrans_transaction(request, data=data)

				Pembelian.objects.filter(kd_transaksi=order.kd_transaksi).update(token=token)

				return redirect('order_view', id=order.kd_transaksi)
			else:
				messages.error(request, "Fill out your information correctly.")

		if len(cart) > 0:
			return render(request, 'order/order.html', context)
		else:
			return redirect('bukus')
	else:
		return redirect('signin')


def order_view(request, id):
    trans = Pembelian.objects.get(pk=id)
    
    context = {
		'subjudul' : "Checkout",
		'order' : trans,
		'token' : trans.token
	}
    return render(request, 'order/detail.html', context)
			
def order_list(request):
	my_order = Pembelian.objects.filter(Akun_id = request.user.id).order_by('tgl_transaksi')
	# print(my_order)
	context = {
		'subjudul' : "Riwayat Pembelian",
		'myorder' : my_order,
	}

	return render(request, 'order/list.html', context)

def order_details(request, id):
	order_summary = get_object_or_404(Pembelian, kd_transaksi=id)

	if order_summary.Akun_id != request.user.id:
		return redirect('resources:index')

	orderedItem = Item_Pembelian.objects.filter(pembelian_id=id)
	context = {
		'subjudul' : "Checkout",
		"o_summary": order_summary,
		"o_item": orderedItem
	}
	return render(request, 'order/details.html', context)

class pdf(View):
    def get(self, request, id):
        try:
            query=get_object_or_404(Pembelian, kd_transaksi=id)
        except:
            Http404('Content not found')
        context={
            "order":query
        }
        article_pdf = renderPdf('order/pdf.html',context)
        return HttpResponse(article_pdf, content_type='application/pdf')


def midtrans_transaction(request, data):
	snap = midtransclient.Snap(
		# Set to true if you want Production Environment (accept real transaction).
		is_production=False,
		server_key='SB-Mid-server-G7Z6wpDHr-WyoLQIn-k0sewq'
	)

	param = {
		"transaction_details": {
			"order_id": data['id_transaksi'],
			"gross_amount": data['payable']
		}, "credit_card":{
			"secure" : True
		}, "customer_details":{
			"first_name": data['nama'],
			"last_name": data['nama_belakang'],
			"email": data['email'],
			"phone": data['telepon']
		}
	}
	
	transaction = snap.create_transaction(param)
	return transaction['token']