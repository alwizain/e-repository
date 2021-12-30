from decimal import Decimal
from django.conf import settings
from resources.models import Buku


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, buku):
        buku_id = str(buku.id_buku)
        if buku_id not in self.cart:
            self.cart[buku_id] = {'jumlah': 0, 'harga': str(buku.harga)}
            self.cart[buku_id]['jumlah'] = 1
        else:    
            if self.cart[buku_id]['jumlah'] < 10:
                self.cart[buku_id]['jumlah'] += 1
        
        self.save()

    def update(self, buku, jumlah):
        buku_id = str(buku.id_buku)
        self.cart[buku_id]['jumlah'] = jumlah
        
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, buku):
        buku_id = str(buku.id_buku)
        if buku_id in self.cart:
            del self.cart[buku_id]
            self.save()

    def __iter__(self):
        buku_ids = self.cart.keys()
        bukus = Buku.objects.filter(id_buku__in=buku_ids)
        for buku in bukus:
            self.cart[str(buku.id_buku)]['buku'] = buku

        for item in self.cart.values():
            item['harga'] = Decimal(item['harga'])
            item['total_harga'] = item['harga'] * item['jumlah']
            yield item

    def __len__(self):
        return sum(item['jumlah'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['harga']) * item['jumlah'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
        
