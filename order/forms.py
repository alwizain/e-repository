from django import forms
from .models import Pembelian

class OrderCreateForm(forms.ModelForm):
	
	class Meta:
		model = Pembelian
		fields = ['nama', "nama_belakang", 'email', 'telepon', 'asal_institusi']
