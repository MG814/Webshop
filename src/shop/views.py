import os
import random

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.shortcuts import redirect
from django.views import View
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView, DeleteView, ListView

from shop.forms import ProductForm, EditForm
from shop.models import Image, Product, Cart, ItemInCart
from shop.mixins import ExtraContextMixin


class HomePageView(ExtraContextMixin, TemplateView):
    template_name = "shop/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = list(Product.objects.all())
        if len(items) >= 3:
            random_items = random.sample(items, 3)
            context['rand_items'] = random_items
        context['products'] = Product.objects.all()
        context['images'] = Image.objects.all().distinct('product')
        return context


class UserProductsPageView(TemplateView):
    template_name = "shop/products/user-products.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['products'] = Product.objects.all()
        context['images'] = Image.objects.all().distinct('product')
        return context


class EditProductView(LoginRequiredMixin, UpdateView):
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
        if img.image:
            if os.path.isfile(img.image.path):
                os.remove(img.image.path)

        img.delete()
        return redirect("product-edit", pk=pk)


class DetailPageView(DetailView):
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
        context['main_images'] = images.distinct('product')

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
        item_in_cart = ItemInCart.objects.filter(product_id=product_id)

        item_in_cart.delete()

        return redirect('user-cart')


def add_to_cart(request):
    if request.method == 'POST':
        user = request.user.id
        product_id_from = request.POST.get('product_id')
        cart_id = Cart.objects.filter(user_id=user).values('id')[0].get('id')
        product_id = Product.objects.filter(id=product_id_from).values('id')[0].get('id')

        product_id_query_set = ItemInCart.objects.filter(cart_id=cart_id).values('product_id')
        product_id_list = [item.get('product_id') for item in product_id_query_set]

        if product_id not in product_id_list:
            new_item_in_cart = ItemInCart(product_id=product_id, cart_id=cart_id)
            new_item_in_cart.save()

        return redirect('user-cart')


def change_quantity(request):
    if request.method == 'POST':
        product_id_from = request.POST.get('product_id')
        operation = request.POST.get('operation')

        item_all = ItemInCart.objects.get(id=product_id_from)
        if operation == 'plus':
            item_all.quantity += 1
        elif operation == 'minus':
            if item_all.quantity > 1:
                item_all.quantity -= 1
        item_all.save()

        return redirect('user-cart')
