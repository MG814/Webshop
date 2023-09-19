from unicodedata import decimal

from .models import ItemInCart, Cart, Image


def get_cart_id(user):
    cart_id = Cart.objects.filter(user_id=user).values('id')[0].get('id')
    return cart_id


def get_items_in_cart(cart_id):
    items_in_cart = ItemInCart.objects.filter(cart_id=cart_id)
    return items_in_cart


def summary_price(cart_id):
    items_in_cart = get_items_in_cart(cart_id)
    total_sum = decimal('0')

    for product_in_cart in items_in_cart:
        total_sum += (product_in_cart.product.price * product_in_cart.quantity)

    return total_sum


def cart_products_id(cart_id):
    id_list = []
    items_in_cart = get_items_in_cart(cart_id)

    for product_in_cart in items_in_cart:
        id_list.append(product_in_cart.product.id)

    return id_list


def get_main_images():
    images = Image.objects.all()
    main_images = images.distinct('product')

    return main_images
