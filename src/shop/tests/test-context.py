from django.test import TestCase
from moneyed import Money

from django.test import tag

import PIL.Image
from django.core.files.base import File
from io import BytesIO

from orders.factory_models import UserFactory, ProductFactory, CartFactory, OrderFactory, ItemFactory
from shop.context_functions import get_user_cart, get_main_images, summary_price, get_orders, get_user_address
from users.models import Address
from products.models import Image, Product


@tag("context")
class TestContextFunctions(TestCase):
    @staticmethod
    def get_image_file(name, ext="png", size=(50, 50), color=(256, 0, 0, 255)):
        file_obj = BytesIO()
        image = PIL.Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def setUp(self) -> None:
        self.user = UserFactory()
        self.user2 = UserFactory()
        self.product = ProductFactory()
        self.cart = CartFactory(user_id=self.user.id)

    def test_get_user_cart(self):
        self.assertEqual(get_user_cart(self.user).id, 1)

    def test_get_orders(self):
        OrderFactory(user_id=self.user.id)
        self.assertEqual(get_orders(self.user).count(), 1)

    def test_summary_price(self):
        self.item_in_cart = ItemFactory(product_id=self.product.id, cart_id=self.cart.id)

        self.assertEqual(summary_price(self.user.id), Money("563", "USD"))

    def test_get_main_images(self):
        p_id = Product.objects.values()[0].get("id")

        jpg = self.get_image_file("test_file")
        jpg2 = self.get_image_file("test_file2")
        image = Image.objects.create(image=jpg, product_id=p_id)
        Image.objects.create(image=jpg2, product_id=p_id)
        self.assertEqual(get_main_images()[0], image)

    def test_get_user_address(self):
        self.assertEqual(get_user_address(self.user2.id), None)
        Address.objects.create(
            user_id=self.user2.id,
            name='Piotr',
            surname='Kowalski',
            locality='Gdansk',
            street='Polna 8',
            zip_code='80-800',
            phone='956-908-123',
        )
        address = Address.objects.filter(user_id=self.user2.id).values()[0]
        self.assertEqual(get_user_address(self.user2.id), address)
