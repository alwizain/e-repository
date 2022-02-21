from django.contrib import admin

# Register your models here.
from .models import Dokumen, Kategori_Dokumen
admin.site.register(Dokumen)
admin.site.register(Kategori_Dokumen)