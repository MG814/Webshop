import os
import random

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.shortcuts import redirect
from django.views import View
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView, DeleteView, ListView
from moneyed import Money

from shop.forms import ProductForm, EditForm
from shop.models import Image, Product, Cart, Item, Review, Order
from shop.mixins import ExtraContextMixin
from shop.context_functions import summary_price, get_user_cart


class HomePageView(ExtraContextMixin, TemplateView):
    template_name = "shop/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = list(Product.objects.all())
        if len(items) >= 3:
            random_items = random.sample(items, 3)
            context['rand_items'] = random_items

        return context


class UserProductsPageView(ExtraContextMixin, TemplateView):
    template_name = "shop/products/user-products.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EditProductView(ExtraContextMixin, LoginRequiredMixin, UpdateView):
    model = Product
    form_class = EditForm
    template_name = 'shop/products/edit.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['images'] = Image.objects.all()
        return context


class DeleteImageView(View):
    def get(self, request, pk, img_id):
        img = Image.objects.get(pk=img_id)
        img.delete()

        if not img.image == 'default_product_pict.jpg':
            os.remove(img.image.path)

        return redirect("product-edit", pk=pk)


class DetailPageView(ExtraContextMixin, DetailView):
    model = Product
    template_name = "shop/products/details.html"

    def post(self, request, pk=None):
        user = self.request.user.id

        product_id = Product.objects.filter(id=pk).values('id')[0].get('id')

        for cart in Cart.objects.filter(user_id=user).all():
            cart_obj = cart

        cart_obj.products.add(product_id)

        return redirect('user-cart')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = Image.objects.all()
        context['images'] = images
        context['stars'] = range(self.object.avg_reviews)
        context['empty_stars'] = range(5 - self.object.avg_reviews)
        return context


class ProductCreateView(ExtraContextMixin, LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/products/add.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        super().form_valid(form)


class DeleteProductView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'shop/products/delete_confirm.html'
    success_url = '/'

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.user


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


class OrdersView(ExtraContextMixin, TemplateView):
    template_name = 'shop/orders/orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.id

        user_orders = Order.objects.filter(user_id=user)

        context['orders'] = user_orders

        return context


class OrderDetailsView(ExtraContextMixin, DetailView):
    model = Item
    template_name = 'shop/orders/order_details.html'


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


def review_product(request, pk=None):
    if request.method == 'POST':
        review = int(request.POST.get('star_rating'))
        product_id_from = Product.objects.filter(id=pk).values('id')[0].get('id')
        user = request.user.id
        review_all = list(Review.objects.filter(user_id=user).values_list('product_id', flat=True))

        if product_id_from not in review_all:
            review = Review.objects.create(user_id=user, product_id=product_id_from, review=review)
            review.save()

        return redirect('product-detail', product_id_from)
