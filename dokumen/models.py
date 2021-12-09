from django.db import models

# Create your models here.
class Dokumen(models.Model):
    kd_dokumen = models.AutoField(primary_key=True)
    nama_dokumen = models.CharField(max_length=100)
    file = models.FileField(upload_to='file/')

    def __str__(self):
        return "{}".format(self.nama_dokumen)