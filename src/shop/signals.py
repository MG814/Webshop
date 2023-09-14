import os

from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from shop.models import Image, Cart


@receiver(post_delete, sender=Image)
def delete_images(sender, instance, **kwargs):
    os.remove(instance.image.path)


@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_cart(sender, instance, **kwargs):
    instance.cart.save()
