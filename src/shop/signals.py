import os

from django.dispatch import receiver
from django.db.models.signals import post_delete
from shop.models import Image


@receiver(post_delete, sender=Image)
def delete_images(sender, instance, **kwargs):
    os.remove(instance.image.path)
