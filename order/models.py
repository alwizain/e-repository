from pyexpat import model
from django.db import models
from resources.models import Buku
from django.contrib.auth.models import User
from datetime import datetime


class Pembelian(models.Model):
	kd_transaksi = models.AutoField(primary_key=True)
	Akun = models.ForeignKey(User, on_delete = models.CASCADE)
	nama = models.CharField(max_length=30)
	email = models.EmailField()
	telepon = models.CharField(max_length=16)
	instansi = models.CharField(max_length=150)
	metode_pembayaran = models.CharField(max_length = 20)
	nomor_akun = models.CharField(max_length = 20)
	payable = models.IntegerField()
	total_buku = models.IntegerField()
	tgl_transaksi = models.DateTimeField(default=datetime.now, blank=True)
	update = models.DateTimeField(auto_now=True)
	bayar = models.BooleanField(default=False)
	token = models.TextField()

	class Meta:
		ordering = ('-tgl_transaksi', )

	def __str__(self):
		return 'Pembelian {}'.format(self.kd_transaksi)

	def get_total_pembelian(self):
		return sum(item.get_cost() for item in self.items.all())


class Item_Pembelian(models.Model):
    kd_item = models.AutoField(primary_key=True)
    pembelian = models.ForeignKey(Pembelian, on_delete=models.CASCADE)
    buku = models.ForeignKey(Buku, on_delete=models.CASCADE)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    jumlah = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.kd_item)

    def get_pembelian(self):
        return self.harga * self.jumlah