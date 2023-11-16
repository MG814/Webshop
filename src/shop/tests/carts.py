from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from moneyed import Money

from django.test import tag
from django.contrib.auth.models import User

import PIL.Image
from django.core.files.base import File
from io import BytesIO

from shop.models import Product, Item, Image
from shop.context_functions import get_user_cart, get_main_images, summary_price


@tag('cart')
class TestCartOperations(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.product = Product.objects.create(user_id=self.user.id, title='test', description='testtest test',
                                              price=Decimal('10'))

    def test_add_item_to_cart(self):
        self.client.force_login(self.user)

        self.assertEqual(Item.objects.count(), 0)
        response = self.client.post(reverse('add-to-cart'), data={'product_id': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Item.objects.count(), 1)

    def test_delete_item_from_cart(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('add-to-cart'), data={'product_id': 2})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Item.objects.count(), 1)

        p_id = Product.objects.values()[0].get('id')
        response = self.client.get(reverse('product-cart-delete', kwargs={'pk': p_id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Item.objects.count(), 0)


@tag('context')
class TestContextFunctions(TestCase):
    @staticmethod
    def get_image_file(name, ext='png', size=(50, 50), color=(256, 0, 0, 255)):
        file_obj = BytesIO()
        image = PIL.Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testuser2',
            password='testpassword2'
        )
        self.user2 = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.product = Product.objects.create(user_id=self.user2.id, title='test2', description='test2test2 2test2',
                                              price=Decimal('10'))

    def test_get_user_cart(self):
        self.assertEqual(get_user_cart(self.user2).id, 4)

    def test_summary_price(self):
        self.item_in_cart = Item.objects.create(quantity=2, product_id=self.product.id,
                                                cart_id=get_user_cart(self.user).id)

        self.assertEqual(summary_price(self.user.id), Money('20.0', 'USD'))

    def test_get_main_images(self):
        p_id = Product.objects.values()[0].get('id')

        jpg = self.get_image_file('test_file')
        jpg2 = self.get_image_file('test_file2')
        image = Image.objects.create(image=jpg, product_id=p_id)
        Image.objects.create(image=jpg2, product_id=p_id)
        self.assertEqual(get_main_images()[0], image)
