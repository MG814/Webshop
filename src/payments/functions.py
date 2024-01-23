from django.core.mail import send_mail
from decimal import Decimal

from orders.models import Order, Delivery


def get_shipping_options(
        shipping_name, shipping_price, max_day_shipping, min_day_shipping
):
    shipping_options = {
        "shipping_rate_data": {
            "type": "fixed_amount",
            "fixed_amount": {"amount": shipping_price * 100, "currency": "usd"},
            "display_name": shipping_name.replace("_", " "),
            "delivery_estimate": {
                "minimum": {"unit": "business_day", "value": min_day_shipping},
                "maximum": {"unit": "business_day", "value": max_day_shipping},
            },
        },
    }
    return shipping_options


def create_new_order(user_id, seller_id, cart, price_amount):
    order = Order(user_id=user_id, seller_id=seller_id)
    order.price_with_shipping.amount = cart.total_price.amount + Decimal(
        price_amount
    )
    order.save()

    return order


def create_new_delivery(name, price, order_id):
    delivery = Delivery(
        name=name, price=price, order_id=order_id
    )
    delivery.save()


def transfer_items_from_cart_to_order(cart, order):
    for item_in_cart in cart.items_in_cart.all():
        item_in_cart.order = order
        item_in_cart.save()
        item_in_cart.cart = None
        item_in_cart.save()
