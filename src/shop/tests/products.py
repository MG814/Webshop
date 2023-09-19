import mock
import PIL.Image
from django.core.files.base import File
from io import BytesIO

from django.test import TestCase
from django.test import tag
from django.test import override_settings

from django.urls import reverse
from decimal import Decimal

from shop.models import Product, Image

from django.contrib.auth.models import User
from djmoney.money import Money


@tag('product')
class TestProductsOperations(TestCase):
    @staticmethod
    def get_image_file(name, ext='png', size=(50, 50), color=(256, 0, 0, 255)):
        file_obj = BytesIO()
        image = PIL.Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.product = Product.objects.create(user_id=self.user.id, title='test', description='testtest test',
                                              price=Decimal('10'))

        self.money = Money(Decimal("10"), "USD")
        self.product = {
            'title': 'product1',
            'description': 'test test',
            "price_0": self.money.amount,
            "price_1": self.money.currency
        }

    def test_add_new_product(self):
        self.client.force_login(self.user)

        self.assertEqual(Product.objects.count(), 1)

        response = self.client.post(reverse('product-add'), data=self.product)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Product.objects.count(), 2)

    def test_delete_product(self):
        self.client.force_login(self.user)

        self.assertEqual(Product.objects.count(), 1)
        p_id = Product.objects.values()[0].get('id')

        response = self.client.post(reverse('product-delete', kwargs={'pk': p_id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 0)

    def test_edit_product(self):
        self.client.force_login(self.user)

        p_id = Product.objects.values()[0].get('id')

        self.money = Money(Decimal("10"), "USD")
        self.edit_product = {
            'title': 'product2',
            'description': 'test testtest testtest test',
            "price_0": self.money.amount,
            "price_1": self.money.currency,
        }

        response = self.client.post(reverse('product-edit', kwargs={'pk': p_id}), data=self.edit_product)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.values()[0].get('title'), 'product2')
        self.assertEqual(Product.objects.values()[0].get('description'), 'test testtest testtest test')
        self.assertEqual(Product.objects.values()[0].get('price'), self.money.amount)

    def test_delete_image(self):
        p_id = Product.objects.values()[0].get('id')

        jpg = self.get_image_file('test_file')
        image = Image.objects.create(image=jpg, product_id=p_id)
        response = self.client.get(reverse('product-image-delete', kwargs={'pk': p_id, 'img_id': image.id}))
        self.assertEqual(response.status_code, 302)
