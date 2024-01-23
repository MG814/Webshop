from django.test import TestCase
from django.test import tag
from django.urls import reverse

from orders.tests.factory_models import OrderFactory, DeliveryFactory


@tag("orders")
class TestOrdersFunctions(TestCase):
    def setUp(self) -> None:
        self.order = OrderFactory()
        self.delivery = DeliveryFactory.create(order=self.order)

    def test_send_order(self):
        tracking = {
            'tracking': '12345678901234567890',
            'operation': 'order_status'
        }

        response = self.client.post(reverse("send", kwargs={"pk": self.order.id}), data=tracking)
        self.assertEqual(response.status_code, 302)
        self.order.refresh_from_db()
        delivery = self.order.delivery.filter(order_id=self.order.id)[0]
        self.assertEqual(self.order.tracking_number, '12345678901234567890')
        self.assertEqual(delivery.status, 'Sent')

    def test_receive_order(self):
        reception_code = {
            'reception_code': 'q34w6',
            'operation': 'order_status',
        }

        response = self.client.post(reverse("receive", kwargs={"pk": self.order.id}), data=reception_code)
        self.assertEqual(response.status_code, 302)
        self.order.refresh_from_db()
        self.assertEqual(self.order.reception_code, 'q34w6')
        delivery = self.order.delivery.filter(order_id=self.order.id)[0]
        self.assertEqual(delivery.status, 'Delivered')
