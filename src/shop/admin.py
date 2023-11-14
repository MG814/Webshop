from django.contrib import admin

from shop.models import Product, Image, Cart, ItemInCart, Review, Order, Delivery
admin.site.register(Image)

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(ItemInCart)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(Delivery)
