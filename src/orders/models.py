from django.core.validators import MinLengthValidator
from django.db import models
from djmoney.models.fields import MoneyField

from core import settings


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='buyer_orders')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='sold_orders')
    price_with_shipping = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
        default="0",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
    tracking_number = models.CharField(blank=True, validators=[MinLengthValidator(20)])
    reception_code = models.CharField(blank=True)


class Delivery(models.Model):
    SHIPPING = (
        ("Free", "Free"),
        ("Next day air", "Next day air"),
    )

    name = models.CharField(max_length=100, choices=SHIPPING, null=True, blank=True)
    price = MoneyField(
        max_digits=14, decimal_places=2, default_currency="USD", null=True, blank=True
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True, blank=True, related_name="delivery"
    )
    status = models.CharField(default='Ordered')
