from _decimal import Decimal

from django.test import TestCase
from django.test import tag
from django.core import mail

from orders.factory_models import UserFactory, CartFactory, OrderFactory, ItemFactory

from orders.models import Order, Delivery
from payments.functions import (
    create_new_order,
    create_new_delivery,
    transfer_items_from_cart_to_order,
    send_email,
    get_shipping_options
)


@tag("payments_functions")
class TestPaymentsFunctions(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.seller = UserFactory()
        self.order = OrderFactory()
        self.cart = CartFactory()

    def test_create_new_order(self):
        self.assertEqual(Order.objects.count(), 1)
        create_new_order(user_id=self.user.id, seller_id=self.seller.id, cart=self.cart, price_amount=1000)
        self.assertEqual(Order.objects.count(), 2)

    def test_create_new_delivery(self):
        self.assertEqual(Delivery.objects.count(), 0)
        create_new_delivery(name='Free', price=15, order_id=self.order.id)
        self.assertEqual(Delivery.objects.count(), 1)

    def test_transfer_items_from_cart_to_order(self):
        ItemFactory(cart_id=self.cart.id)

        self.assertEqual(self.cart.items_in_cart.count(), 1)
        self.assertEqual(self.order.items_in_order.count(), 0)

        transfer_items_from_cart_to_order(self.cart, self.order)

        self.assertEqual(self.cart.items_in_cart.count(), 0)
        self.assertEqual(self.order.items_in_order.count(), 1)

    def test_send_email(self):
        send_email('test.com')
        first_message = mail.outbox[0]

        self.assertEqual(first_message.subject, 'GridShop: Successful Payment')
        self.assertEqual(first_message.body, 'test.com')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(first_message.from_email, 'wenomus@gmail.com')
        self.assertEqual(first_message.to, ['keponel538@ziragold.com'])

    def test_get_shipping_options(self):
        options = get_shipping_options('Next_day', 0.2, 15, 3)

        rate_data = options.get('shipping_rate_data')
        fixed_amount = rate_data.get('fixed_amount')
        amount = fixed_amount.get('amount')
        currency = fixed_amount.get('currency')
        self.assertEqual(amount, 20)
        self.assertEqual(currency, 'usd')

        delivery_name = rate_data.get('display_name')
        self.assertEqual(delivery_name, 'Next day')

        delivery_estimate = rate_data.get('delivery_estimate')
        maximum = delivery_estimate.get('maximum')
        maximum_value = maximum.get('value')
        minimum = delivery_estimate.get('minimum')
        minimum_value = minimum.get('value')
        self.assertEqual(maximum_value, 15)
        self.assertEqual(minimum_value, 3)

