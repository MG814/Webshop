import factory
from djmoney.money import Money
from faker import Faker
from faker.providers import BaseProvider
from moneyed import USD

from products.models import Product
from shop.models import Cart, Item
from users.models import User
from orders.models import Order, Delivery


class MoneyProvider(BaseProvider):
    def money(self):
        return Money(563, USD)


fake = Faker()
fake.add_provider(MoneyProvider)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('name')


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    user = factory.SubFactory(UserFactory)
    title = fake.pystr()
    price = fake.money()


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    seller = factory.SubFactory(UserFactory)


class DeliveryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Delivery

    order = factory.SubFactory(OrderFactory)


class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    user = factory.SubFactory(UserFactory)


class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    product = factory.SubFactory(ProductFactory)
    cart = factory.SubFactory(CartFactory)
