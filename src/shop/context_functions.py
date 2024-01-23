from unicodedata import decimal

from users.models import Address
from products.models import Image
from .models import Cart
from orders.models import Order


def get_user_cart(user_id):
    cart = Cart.objects.filter(user_id=user_id)[0]
    return cart


def get_orders(user_id):
    orders = Order.objects.filter(user_id=user_id)
    return orders


def summary_price(user_id):
    cart = get_user_cart(user_id)
    total_sum = decimal('0')

    for product_in_cart in cart.items_in_cart.all():
        total_sum += (product_in_cart.product.price * product_in_cart.quantity)

    return total_sum


def get_main_images():
    images = Image.objects.all()
    main_images = images.distinct('product')

    return main_images


def get_user_address(user_id):
    if Address.objects.filter(user_id=user_id).exists():
        address = Address.objects.filter(user_id=user_id).values()[0]
        return address
