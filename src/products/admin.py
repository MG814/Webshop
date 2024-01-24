from django.contrib import admin

from products.models import Product, Image, Review, Wishlist, WishlistItem

admin.site.register(Image)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Wishlist)
admin.site.register(WishlistItem)