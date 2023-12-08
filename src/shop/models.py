from django.contrib.auth.models import User
from django.db import models
from djmoney.models.fields import MoneyField


class Product(models.Model):
    CATEGORY_CHOICES = (
        ('Other', 'Other'),
        ('Beauty', 'Beauty'),
        ('Electronics', 'Electronics'),
        ('Fashion', 'Fashion'),
        ('Home and Garden', 'Home and Garden'),
        ('Motorization', 'Motorization'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=500, blank=True)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', currency_choices=[('USD', 'USD $')])
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='')
    created_at = models.DateTimeField(auto_created=True, auto_now=True)

    @property
    def avg_reviews(self):
        if self.reviews.all().count() > 0:
            return int(sum([review.review for review in self.reviews.all()]) / self.reviews.all().count())
        return 0


class Image(models.Model):
    image = models.FileField(upload_to='product_pics')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')


class Cart(models.Model):
    total_price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', default='0')
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price_with_shipping = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', default='0', null=True,
                                     blank=True)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)


class Item(models.Model):
    quantity = models.PositiveIntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True, related_name='items_in_cart')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='items_in_order')

    @property
    def sum_one_item(self):
        return self.product.price * self.quantity


class Delivery(models.Model):
    SHIPPING = (
        ('Free', 'Free'),
        ('Next day air', 'Next day air'),
    )

    name = models.CharField(max_length=100, choices=SHIPPING, null=True, blank=True)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='delivery')


class Review(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    review = models.FloatField(default=0.0)
