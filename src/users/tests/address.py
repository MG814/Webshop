from django.test import TestCase
from django.urls import reverse

from django.test import tag

from users.models import Address, User


@tag("address")
class TestAddressOperations(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.address = Address.objects.create(
            user_id=self.user.id,
            name='Piotr',
            surname='Kowalski',
            locality='Gdansk',
            street='Polna 8',
            zip_code='80-800',
            phone='956-908-123',
        )

        self.address2 = {
            'user_id': self.user.id,
            'name': 'Paweł',
            'surname': 'Nowak',
            'locality': 'Warszawa',
            'street': 'Pomorska',
            'zip_code': '20-000',
            'phone': '902-387-123',
        }

    def test_add_new_address(self):
        self.client.force_login(self.user)

        self.assertEqual(Address.objects.count(), 1)

        response = self.client.post(reverse("address-add"), data=self.address2)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(Address.objects.count(), 2)

    def test_edit_address(self):
        self.client.force_login(self.user)

        p_id = Address.objects.values()[0].get("id")

        self.edit_address = {
            "name": "Paweł",
            "surname": "Nowak",
            "locality": 'Warszawa',
            "street": 'Nowa 45',
            "zip_code": "20-200",
            "phone": "345-899-340",
        }

        response = self.client.post(
            reverse("address-edit", kwargs={"pk": p_id}), data=self.edit_address
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Address.objects.values()[0].get("name"), "Paweł")
        self.assertEqual(Address.objects.values()[0].get("surname"), "Nowak")
        self.assertEqual(Address.objects.values()[0].get("locality"), "Warszawa")
        self.assertEqual(Address.objects.values()[0].get("street"), "Nowa 45")
        self.assertEqual(Address.objects.values()[0].get("zip_code"), "20-200")
        self.assertEqual(Address.objects.values()[0].get("phone"), "345-899-340")
