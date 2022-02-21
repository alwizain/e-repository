from django.db import models

# Create your models here.
class Dokumen(models.Model):
    kd_dokumen = models.AutoField(primary_key=True)
    kategori_dok = models.ForeignKey('Kategori_Dokumen', on_delete = models.CASCADE, default=1)
    nama_dokumen = models.CharField(max_length=100)
    file = models.FileField(upload_to='file/')

    def __str__(self):
        return "{}".format(self.nama_dokumen)

class Kategori_Dokumen(models.Model):
    id_kategori = models.AutoField(primary_key=True)
    nama_kategori = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nama_kategori