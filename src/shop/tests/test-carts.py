from django.test import TestCase
from django.urls import reverse

from django.test import tag

from orders.factory_models import UserFactory, ProductFactory, CartFactory
from shop.models import Item
from products.models import Product


@tag("cart")
class TestCartOperations(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.product = ProductFactory()
        CartFactory(user_id=self.user.id)

    def test_add_item_to_cart(self):
        self.client.force_login(self.user)

        self.assertEqual(Item.objects.count(), 0)
        response = self.client.post(reverse("add-to-cart"), data={"product_id": self.product.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Item.objects.count(), 1)

    def test_delete_item_from_cart(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("product-cart-add"), data={"product_id": self.product.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Item.objects.count(), 1)

        p_id = Product.objects.values()[0].get("id")
        response = self.client.get(reverse("product-cart-delete", kwargs={"pk": p_id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Item.objects.count(), 0)
