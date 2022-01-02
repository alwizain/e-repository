from django import forms
from .models import Pembelian

class OrderCreateForm(forms.ModelForm):
	PAYMENT_METHOD_CHOICES = (
		('Rocket', 'Rocket'),
		('Bkash','Bkash')
	)

	metode_pembayaran = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES, widget=forms.RadioSelect())

	class Meta:
		model = Pembelian
		fields = ['nama', 'email', 'telepon', 'instansi', 'metode_pembayaran', 'nomor_akun']
