# cart/cart.py
# cart/cart.py
from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, size, quantity=1):
        key = f"{product.id}-{size}"
        if key not in self.cart:
            self.cart[key] = {
                'product_id': str(product.id),
                'name': product.name,
                'price': str(product.price),
                'quantity': 0,
                'size': size
            }
        self.cart[key]['quantity'] += quantity
        self.save()

    def remove(self, key):
        if key in self.cart:
            del self.cart[key]
            self.save()

    def save(self):
        self.session.modified = True

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def __iter__(self):
        product_ids = [item['product_id'] for item in self.cart.values()]
        products = Product.objects.filter(id__in=product_ids)
        products_dict = {str(p.id): p for p in products}

        for key, item in self.cart.items():
            product = products_dict.get(item['product_id'])
            item = item.copy()
            item['product'] = product
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            item['key'] = key
            yield item

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()







# from decimal import Decimal
# from django.conf import settings
# from shop.models import Product


# class Cart(object):
#     def __init__(self, request):
#         self.session = request.session
#         cart = self.session.get(settings.CART_SESSION_ID)
#         if not cart:
#             cart = self.session[settings.CART_SESSION_ID] = {}
#         self.cart = cart

#     def add(self, product, size, quantity=1, override_quantity=False):
#         # Ключ — id_размер, чтобы можно было добавить один и тот же товар разных размеров
#         key = f"{product.id}_{size}"
#         if key not in self.cart:
#             self.cart[key] = {
#                 'product_id': str(product.id),
#                 'name': product.name,
#                 'price': str(product.price),
#                 'quantity': 0,
#                 'size': size,
#                 'image': product.image.url if product.image else ''
#             }
#         if override_quantity:
#             self.cart[key]['quantity'] = quantity
#         else:
#             self.cart[key]['quantity'] += quantity
#         self.save()

#     def save(self):
#         self.session.modified = True

#     def remove(self, key):
#         if key in self.cart:
#             del self.cart[key]
#             self.save()

#     def __iter__(self):
#         for item in self.cart.values():
#             item['price'] = Decimal(item['price'])
#             item['total_price'] = item['price'] * item['quantity']
#             yield item

#     def __len__(self):
#         return sum(item['quantity'] for item in self.cart.values())

#     def get_total_price(self):
#         return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

#     def clear(self):
#         del self.session[settings.CART_SESSION_ID]
#         self.save()