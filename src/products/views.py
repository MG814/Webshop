import os

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.shortcuts import redirect
from django.views import View
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView, DeleteView

from products.forms import ProductForm, EditForm
from products.models import Image, Product
from shop.models import Cart
from shop.mixins import ExtraContextMixin


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
