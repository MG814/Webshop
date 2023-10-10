from django.contrib.auth.models import User
from django.db import models
from djmoney.models.fields import MoneyField


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=500)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    created_at = models.DateTimeField(auto_created=True, auto_now=True)

    @property
    def avg_reviews(self):
        if self.reviews.all().count() != 0:
            return int(sum([review.review for review in self.reviews.all()]) / self.reviews.all().count())
        else:
            return 0


class Image(models.Model):
    image = models.FileField(upload_to='product_pics')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')


class Cart(models.Model):
    total_price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', default='0')
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class ItemInCart(models.Model):
    quantity = models.PositiveIntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    review = models.FloatField(default=0.0)
