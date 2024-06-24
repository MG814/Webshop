from django.core.mail import send_mail

from django.conf import settings


def send_email(receipt_url, buyer_email) -> None:
    send_mail(subject='GridShop: Successful Payment',
              message=f'{receipt_url}',
              from_email=settings.DEFAULT_EMAIL,
              recipient_list=[buyer_email],
              fail_silently=False
              )
