import os
import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView

from shop.forms import ProductForm, EditForm
from shop.models import Image, Product


class HomePageView(TemplateView):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = Image.objects.all()
        context['images'] = images
        context['main_images'] = images.distinct('product')
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/products/add.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
