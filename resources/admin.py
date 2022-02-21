from django.contrib import admin
from . models import Buku, Journal, Kategori_Journal, Pengarang, Kategori, Review, UserRating

# Register your models here.
admin.site.register(Buku)
admin.site.register(Journal)
admin.site.register(Pengarang)
admin.site.register(Kategori)
admin.site.register(Kategori_Journal)
admin.site.register(Review)
admin.site.register(UserRating)
