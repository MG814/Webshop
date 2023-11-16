from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView
from moneyed import Money

from shop.models import Product, Cart, Item, Review
from shop.mixins import ExtraContextMixin
from shop.context_functions import summary_price, get_user_cart


class CartUserView(ExtraContextMixin, ListView):
    model = Cart
    template_name = 'shop/user-cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.id
        cart = get_user_cart(user)

        s = summary_price(user)
        cart.total_price = s
        cart.save()

        context['total_price'] = cart.total_price

        return context


class CartHomePageView(ExtraContextMixin, ListView):
    model = Cart
    template_name = 'shop/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeleteCartProductView(View):
    def get(self, request, pk):
        product_id = Product.objects.filter(id=pk).values('id')[0].get('id')
        item_in_cart = Item.objects.filter(product_id=product_id)

        item_in_cart.delete()

        return redirect('user-cart')


def add_to_cart(request):
    if request.method == 'POST':
        user = request.user.id
        product_id_from = request.POST.get('product_id')
        cart_id = Cart.objects.filter(user_id=user).values('id')[0].get('id')
        product_id = Product.objects.filter(id=product_id_from).values('id')[0].get('id')

        product_id_query_set = Item.objects.filter(cart_id=cart_id).values('product_id')
        product_id_list = [item.get('product_id') for item in product_id_query_set]

        if product_id not in product_id_list:
            new_item_in_cart = Item(product_id=product_id, cart_id=cart_id)
            new_item_in_cart.save()

        return redirect('user-cart')


def change_quantity(request):
    if request.method == 'POST':
        product_id_from = request.POST.get('product_id')
        operation = request.POST.get('operation')

        item_all = Item.objects.get(id=product_id_from)
        if operation == 'plus':
            item_all.quantity += 1
        elif operation == 'minus':
            if item_all.quantity > 1:
                item_all.quantity -= 1
        item_all.save()

        return redirect('user-cart')


def total_price_view(request):
    if request.method == 'POST':
        user = request.user.id
        delivery = request.POST.get('delivery')
        cart = get_user_cart(user)

        cart.total_price = Money('0', 'USD')
        cart.save()

        if delivery == 'option1':
            cart.total_price = Money('10', 'USD')
            cart.save()
        elif delivery == 'option2':
            cart.total_price = Money('5', 'USD')
            cart.save()

    return redirect('user-cart')
