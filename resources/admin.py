from django.contrib import admin
from . models import Buku, Journal, Pengarang, Kategori, Review

# Register your models here.
admin.site.register(Buku)
admin.site.register(Journal)
admin.site.register(Pengarang)
admin.site.register(Kategori)
admin.site.register(Review)
