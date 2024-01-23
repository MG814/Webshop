import factory
from users.models import User
from orders.models import Order, Delivery


class DeliveryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Delivery


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('name')


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order
        django_get_or_create = (
            'user', 'seller', 'tracking_number', 'reception_code')

    user = factory.SubFactory(UserFactory)
    seller = factory.SubFactory(UserFactory)
    tracking_number = ''
    reception_code = ''
