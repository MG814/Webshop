from django.db import models
from djmoney.models.fields import MoneyField
from orders.models import Order
from products.models import Product

from core import settings


class Cart(models.Model):
    total_price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', default='0')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Item(models.Model):
    quantity = models.PositiveIntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True, related_name='items_in_cart')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='items_in_order')

    @property
    def sum_one_item(self):
        return self.product.price * self.quantity
