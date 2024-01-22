from PIL import Image
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    role = models.CharField(
        max_length=6,
        choices=[('Seller', 'Seller'), ('Buyer', 'Buyer')]
    )


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 100 or img.width > 100:
            output_size = (100, 100)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return f'Profile of {self.user.username}'


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    locality = models.CharField(max_length=25)
    street = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=6)
    phone = models.CharField(max_length=15)

