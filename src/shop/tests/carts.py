from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from moneyed import Money

from django.test import tag
from django.contrib.auth.models import User

import PIL.Image
from django.core.files.base import File
from io import BytesIO

from shop.models import Product, ItemInCart, Image
from shop.context_functions import get_cart_id, get_items_in_cart, get_main_images, summary_price, \
    cart_products_id


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

        self.assertEqual(ItemInCart.objects.count(), 0)
        response = self.client.post(reverse('add-to-cart'), data={'product_id': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ItemInCart.objects.count(), 1)

    def test_delete_item_from_cart(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('add-to-cart'), data={'product_id': 2})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ItemInCart.objects.count(), 1)

        p_id = Product.objects.values()[0].get('id')
        response = self.client.get(reverse('product-cart-delete', kwargs={'pk': p_id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ItemInCart.objects.count(), 0)


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
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpassword2'
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.product = Product.objects.create(user_id=self.user2.id, title='test2', description='test2test2 2test2',
                                              price=Decimal('10'))
        self.product2 = Product.objects.create(user_id=self.user2.id, title='test2', description='test2test2 2test2',
                                               price=Decimal('89.9'))

        self.cart_id = get_cart_id(self.user2)
        self.items_in_cart = ItemInCart.objects.create(quantity=4, product=self.product2, cart_id=self.cart_id)
        self.items_in_cart2 = ItemInCart.objects.create(quantity=2, product=self.product, cart_id=self.cart_id)

    def test_get_cart_id(self):
        self.assertEqual(get_cart_id(self.user2), 3)

    def test_get_items_in_cart(self):
        items_in_cart_list = [self.items_in_cart, self.items_in_cart2]
        self.assertEqual(get_items_in_cart(self.cart_id).count(), 2)

        self.assertEqual(get_items_in_cart(self.cart_id).values()[0].get('quantity'), items_in_cart_list[0].quantity)
        self.assertEqual(get_items_in_cart(self.cart_id).values()[0].get('product_id'), items_in_cart_list[0].product_id)
        self.assertEqual(get_items_in_cart(self.cart_id).values()[0].get('cart_id'), items_in_cart_list[0].cart_id)

        self.assertEqual(get_items_in_cart(self.cart_id).values()[1].get('quantity'), items_in_cart_list[1].quantity)
        self.assertEqual(get_items_in_cart(self.cart_id).values()[1].get('product_id'), items_in_cart_list[1].product_id)
        self.assertEqual(get_items_in_cart(self.cart_id).values()[1].get('cart_id'), items_in_cart_list[1].cart_id)

    def test_summary_price(self):
        self.assertEqual(summary_price(self.cart_id), Money('379.6', 'USD'))

    def test_cart_products_id(self):
        self.assertEqual(cart_products_id(self.cart_id), [2, 1])

    def test_get_main_images(self):
        p_id = Product.objects.values()[0].get('id')

        jpg = self.get_image_file('test_file')
        jpg2 = self.get_image_file('test_file2')
        image = Image.objects.create(image=jpg, product_id=p_id)
        Image.objects.create(image=jpg2, product_id=p_id)
        self.assertEqual(get_main_images()[0], image)
