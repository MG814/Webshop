from unicodedata import decimal

from users.models import Address
from .models import Cart
from products.models import Image, Wishlist
from orders.models import Order


def get_user_cart(user_id):
    cart = Cart.objects.filter(user_id=user_id)[0]
    return cart


def get_orders(user_id):
    orders = Order.objects.filter(user_id=user_id)
    return orders


def get_wishlist(user_id):
    wishlist = Wishlist.objects.filter(user_id=user_id)[0]
    return wishlist


def summary_price(user_id):
    cart = get_user_cart(user_id)
    total_sum = decimal("0")

    for product_in_cart in cart.items_in_cart.all():
        total_sum += product_in_cart.discounted_price * product_in_cart.quantity

    return total_sum


def get_main_images():
    images = Image.objects.all()
    main_images = images.distinct("product")

    return main_images


def get_user_address(user_id):
    if Address.objects.filter(user_id=user_id).exists():
        address = Address.objects.filter(user_id=user_id).values()[0]
    else:
        address = None
    return address
