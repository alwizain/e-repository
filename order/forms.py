from django import forms
from .models import Pembelian

class OrderCreateForm(forms.ModelForm):
	DIVISION_CHOICES = (
		('Dhaka', 'Dhaka'),
		('Chattagram', 'Chattagram'),
		('Rajshahi', 'Rajshahi '),
	)

	DISCRICT_CHOICES = (
		('Dhaka', 'Dhaka'), 
		('Gazipur', 'Gazipur'),
		('Narayanganj', 'Narayanganj'),
	)

	PAYMENT_METHOD_CHOICES = (
		('Rocket', 'Rocket'),
		('Bkash','Bkash')
	)

	kota = forms.ChoiceField(choices=DIVISION_CHOICES)
	kabupaten =  forms.ChoiceField(choices=DISCRICT_CHOICES)
	metode_pembayaran = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES, widget=forms.RadioSelect())

	class Meta:
		model = Pembelian
		fields = ['nama', 'email', 'telepon', 'alamat', 'kota', 'kabupaten', 'kode_pos', 'metode_pembayaran', 'nomor_akun']
