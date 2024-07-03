from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from djmoney.models.fields import MoneyField
from django.conf import settings


class Product(models.Model):
    CATEGORY_CHOICES = (
        ("Other", "Other"),
        ("Beauty", "Beauty"),
        ("Electronics", "Electronics"),
        ("Fashion", "Fashion"),
        ("Home and Garden", "Home and Garden"),
        ("Motorization", "Motorization"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=250,
    )
    description = models.TextField(
        max_length=500,
        blank=True,
    )
    price = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
        currency_choices=[("USD", "USD $")],
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default="",
    )
    created_at = models.DateTimeField(
        auto_created=True,
        auto_now=True,
    )
    discount_code = models.CharField(
        max_length=50,
        blank=True,
    )
    discount_percent = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ],
    )

    @property
    def avg_reviews(self):
        if self.reviews.all().count() > 0:
            return int(
                sum([review.review for review in self.reviews.all()])
                / self.reviews.all().count()
            )
        return 0

    @property
    def stars(self):
        return range(self.avg_reviews)

    @property
    def empty_stars(self):
        return range(5 - self.avg_reviews)


class Image(models.Model):
    image = models.FileField(upload_to="product_pics")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    review = models.FloatField(default=0.0)


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class WishlistItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlistitems")
    wishlist = models.ForeignKey(
        Wishlist,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="items_in_wishlist",
    )