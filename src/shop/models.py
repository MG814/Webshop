from django.contrib.auth.models import User
from django.db import models
from djmoney.models.fields import MoneyField


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=500)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    created_at = models.DateTimeField(auto_created=True, auto_now=True)


class Image(models.Model):
    image = models.FileField(upload_to='product_pics')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

