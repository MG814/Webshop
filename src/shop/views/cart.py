from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views import View
from django.views.generic import ListView, DeleteView

from shop.models import Product, Cart, Item
from shop.mixins import ExtraContextMixin
from shop.context_functions import summary_price, get_user_cart
from users.models import Address
from django.contrib import messages


class CartUserView(ExtraContextMixin, ListView):
    model = Cart
    template_name = 'shop/user-cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.id
        cart = get_user_cart(user)
        address = Address.objects.filter(user_id=user)

        if address.count() == 0:
            context['site'] = reverse_lazy('address')
        else:
            context['site'] = reverse_lazy('create-checkout-session')

        sum_price = summary_price(user)
        cart.total_price = sum_price
        cart.save()

        context['total_price'] = cart.total_price

        return context


class DeleteCartProductView(DeleteView):
    model = Item
    success_url = reverse_lazy("cart")


class AddToCart(View):
    def post(self, request, *args, **kwargs):
        user = request.user.id
        pr_id = kwargs.get('pk')
        cart_id = Cart.objects.filter(user_id=user).values("id")[0].get("id")
        product_id = Product.objects.filter(id=pr_id).values("id")[0].get("id")

        seller_id = Product.objects.filter(id=pr_id).values("user")[0].get("user")

        product_id_query_set = Item.objects.filter(cart_id=cart_id).values("product_id")
        product_id_list = [item.get("product_id") for item in product_id_query_set]

        seller_id_cart_item = seller_id
        if len(product_id_list) > 0:
            seller_id_cart_item = Product.objects.filter(id=product_id_list[0]).values("user")[0].get("user")

        if seller_id == seller_id_cart_item:
            if product_id not in product_id_list:
                new_item_in_cart = Item(product_id=product_id, cart_id=cart_id)
                new_item_in_cart.save()
            return redirect("cart")
        else:
            messages.info(request, "Your cart contains items from another seller.")
            return redirect("home")


class ChangeQuantity(View):
    def post(self, request):
        product_id_from = request.POST.get("product_id")
        operation = request.POST.get("operation")

        item_all = Item.objects.get(id=product_id_from)
        if operation == "plus":
            item_all.quantity += 1
        elif operation == "minus":
            if item_all.quantity > 1:
                item_all.quantity -= 1
        item_all.save()

        return redirect("cart")
