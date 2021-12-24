from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from cart.cart import Cart
from .models import Pembelian, Item_Pembelian
from .forms import OrderCreateForm
from .pdfcreator import renderPdf

def order_create(request):
	cart = Cart(request)
	if request.user.is_authenticated:
		akun = get_object_or_404(User, id=request.user.id)
		form = OrderCreateForm(request.POST or None, initial={"nama": akun.first_name, "email": akun.email})
		if request.method == 'POST':
			if form.is_valid():
				order = form.save(commit=False)
				order.Akun = User.objects.get(id=request.user.id)
				order.payable = cart.get_total_harga()
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
				return render(request, 'order/successfull.html', {'pembelian': order})

			else:
				messages.error(request, "Fill out your information correctly.")

		if len(cart) > 0:
			return render(request, 'order/order.html', {"form": form})
		else:
			return redirect('resources:bukus')
	else:
		return redirect('signin')
			
def order_list(request):
	my_order = Pembelian.objects.filter(Akun_id = request.user.id).order_by('-created')
	paginator = Paginator(my_order, 5)
	page = request.GET.get('page')
	myorder = paginator.get_page(page)

	return render(request, 'order/list.html', {"myorder": myorder})

def order_details(request, id):
	order_summary = get_object_or_404(Pembelian, kd_transaksi=id)

	if order_summary.Akun_id != request.user.id:
		return redirect('resources:index')

	orderedItem = Item_Pembelian.objects.filter(pembelian_id=id)
	context = {
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
        return HttpResponse(article_pdf,content_type='application/pdf')
