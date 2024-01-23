from django.contrib import admin

from products.models import Product, Image, Review

admin.site.register(Image)
admin.site.register(Product)
admin.site.register(Review)
