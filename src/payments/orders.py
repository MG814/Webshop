from decimal import Decimal

from orders.models import Order, Delivery


def create_new_order(user_id, seller_id, cart, price_amount) -> Order:
    order = Order(user_id=user_id, seller_id=seller_id)
    order.price_with_shipping.amount = cart.total_price.amount + Decimal(
        price_amount
    )
    order.save()

    return order


def create_new_delivery(name, price, order_id) -> None:
    delivery = Delivery(
        name=name, price=price, order_id=order_id
    )
    delivery.save()


def transfer_items_from_cart_to_order(cart, order) -> None:
    for item_in_cart in cart.items_in_cart.all():
        item_in_cart.order = order
        item_in_cart.save()
        item_in_cart.cart = None
        item_in_cart.save()
