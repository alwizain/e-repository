from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Journal(models.Model):
    kd_jurnal = models.AutoField(primary_key=True)
    kategorij = models.ForeignKey('Kategori_Journal', on_delete = models.CASCADE)
    jdl_jurnal = models.CharField(max_length=100)
    pengarang = models.CharField(max_length=100)
    terbitan = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    abstract = models.TextField()
    refrensi = models.TextField()
    keywords = models.CharField(max_length=50)
    file = models.FileField(upload_to='file/')

    def __str__(self):
        return "{}".format(self.jdl_jurnal)

class Pengarang(models.Model):
    id_pengarang = models.AutoField(primary_key=True)
    nama_pengarang = models.CharField(max_length=100)
    deskripsi_pengarang = models.CharField(max_length=100)
    foto = models.FileField(upload_to='file/foto')

    def __str__(self):
        return self.nama_pengarang

class Kategori(models.Model):
    id_kategori = models.AutoField(primary_key=True)
    nama_kategori = models.CharField(max_length=50)

    def __str__(self):
        return "{}".format(self.nama_kategori)

class Kategori_Journal(models.Model):
    id_kategorij = models.AutoField(primary_key=True)
    nama_kategori = models.CharField(max_length=50)

    def __str__(self):
        return "{}".format(self.nama_kategori)


class Buku(models.Model):
    id_buku = models.AutoField(primary_key=True)
    kategori = models.ForeignKey('Kategori', on_delete = models.CASCADE)
    pengarang = models.ForeignKey('Pengarang', on_delete = models.CASCADE)
    jdl_buku = models.CharField(max_length=100)
    harga = models.CharField(max_length=10)
    stok = models.IntegerField()
    cover = models.FileField(upload_to='file/cover')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    totalreview = models.IntegerField(default=1)
    totalrating = models.IntegerField(default=1)
    status = models.IntegerField(default=1)
    deskripsi = models.TextField()
    file = models.FileField(upload_to='file/buku')
    
    def __str__(self):
        return "{}".format(self.jdl_buku)

class Review(models.Model):
	reviewer = models.ForeignKey(User, on_delete = models.CASCADE)
	buku = models.ForeignKey(Buku, on_delete = models.CASCADE)
	review_star = models.IntegerField()
	review_text = models.TextField()
	created = models.DateTimeField(auto_now_add=True)