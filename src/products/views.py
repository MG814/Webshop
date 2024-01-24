import os

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    TemplateView,
    DetailView,
    UpdateView,
    DeleteView, ListView,
)

from products.forms import ProductForm, EditForm
from products.models import Image, Product, Review, Wishlist, WishlistItem
from shop.models import Cart
from shop.mixins import ExtraContextMixin


class UserProductsPageView(ExtraContextMixin, TemplateView):
    template_name = "products/user_products.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EditProductView(ExtraContextMixin, LoginRequiredMixin, UpdateView):
    model = Product
    form_class = EditForm
    template_name = "products/edit.html"
    success_url = "/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["images"] = Image.objects.all()
        return context


class DeleteImageView(DeleteView):
    def get(self, request, pk=None, img_id=None, *args, **kwargs):
        img = get_object_or_404(Image, pk=img_id)
        img.delete()

        if not img.image == "default_product_pict.jpg":
            os.remove(img.image.path)

        return redirect("product-edit", pk=pk)


class DetailPageView(ExtraContextMixin, DetailView):
    model = Product
    template_name = "products/details.html"

    def post(self, request, pk=None):
        user = self.request.user.id
        product = get_object_or_404(Product, pk=pk)

        for cart in Cart.objects.filter(user_id=user).all():
            cart_obj = cart

        cart_obj.products.add(product.id)

        return redirect("user-cart")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = Image.objects.all()
        context["images"] = images
        return context


class ProductCreateView(ExtraContextMixin, LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/add.html"
    success_url = "/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        super().form_valid(form)


class DeleteProductView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = "products/delete_confirm.html"
    success_url = "/"

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.user


class ReviewProduct(View):
    def post(self, request, pk):
        review = int(request.POST.get("star_rating"))
        product = get_object_or_404(Product, pk=pk)
        user = request.user.id
        review_all = list(
            Review.objects.filter(user_id=user).values_list("product_id", flat=True)
        )

        if product.id not in review_all:
            review = Review.objects.create(
                user_id=user, product_id=product.id, review=review
            )
            review.save()

        return redirect("product-detail", product.id)


class WishlistView(ExtraContextMixin, ListView):
    model = Wishlist
    template_name = "products/wishlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeleteWishlistProductView(DeleteView):
    model = WishlistItem
    success_url = reverse_lazy("wishlist")


class AddToWishList(View):
    def post(self, request):
        user = request.user.id
        product_id_from = request.POST.get("product_id")
        wishlist_id = Wishlist.objects.filter(user_id=user).values("id")[0].get("id")
        product_id = (
            Product.objects.filter(id=product_id_from).values("id")[0].get("id")
        )

        product_id_query_set = WishlistItem.objects.filter(wishlist_id=wishlist_id).values("product_id")
        product_id_list = [item.get("product_id") for item in product_id_query_set]

        if product_id not in product_id_list:
            new_item_in_wishlist = WishlistItem(product_id=product_id, wishlist_id=wishlist_id)
            new_item_in_wishlist.save()

        return redirect("wishlist")
