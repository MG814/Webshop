from django.test import TestCase
from django.test import tag
from django.urls import reverse

from orders.factory_models import DeliveryFactory


@tag("orders")
class TestOrdersFunctions(TestCase):
    def setUp(self) -> None:
        self.delivery = DeliveryFactory()

    def test_send_order(self):
        tracking = {
            'tracking': '12345678901234567890',
            'operation': 'order_status'
        }

        response = self.client.post(reverse("send", kwargs={"pk": self.delivery.order.id}), data=tracking)
        self.assertEqual(response.status_code, 302)
        self.delivery.refresh_from_db()

        self.assertEqual(self.delivery.order.tracking_number, '12345678901234567890')
        self.assertEqual(self.delivery.status, 'Sent')

    def test_receive_order(self):
        reception_code = {
            'reception_code': 'q34w6',
            'operation': 'order_status',
        }

        response = self.client.post(reverse("receive", kwargs={"pk": self.delivery.order.id}), data=reception_code)
        self.assertEqual(response.status_code, 302)
        self.delivery.refresh_from_db()
        self.assertEqual(self.delivery.order.reception_code, 'q34w6')
        self.assertEqual(self.delivery.status, 'Delivered')
