from django.contrib import admin

from shop.models import Product, Image, Cart, ItemInCart

admin.site.register(Product)
admin.site.register(Image)

admin.site.register(Cart)
admin.site.register(ItemInCart)
