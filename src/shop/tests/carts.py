from django.test import TestCase
from django.urls import reverse
from decimal import Decimal

from django.test import tag

from shop.models import Item
from users.models import User
from products.models import Product


@tag("cart")
class TestCartOperations(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.product = Product.objects.create(
            user_id=self.user.id,
            title="test",
            description="testtest test",
            price=Decimal("10"),
        )

    def test_add_item_to_cart(self):
        self.client.force_login(self.user)

        self.assertEqual(Item.objects.count(), 0)
        response = self.client.post(reverse("add-to-cart"), data={"product_id": 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Item.objects.count(), 1)

    def test_delete_item_from_cart(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("add-to-cart"), data={"product_id": 2})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Item.objects.count(), 1)

        p_id = Product.objects.values()[0].get("id")
        response = self.client.get(reverse("product-cart-delete", kwargs={"pk": p_id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Item.objects.count(), 0)
