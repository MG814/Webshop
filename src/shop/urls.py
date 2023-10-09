from django.urls import path

from .views import HomePageView, ProductCreateView, DetailPageView, UserProductsPageView, EditProductView, \
    DeleteImageView, DeleteProductView, CartUserView, DeleteCartProductView, add_to_cart, change_quantity, \
    review_product

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('product/add/', ProductCreateView.as_view(), name='product-add'),
    path('product/details/<int:pk>/', DetailPageView.as_view(), name='product-detail'),
    path('product/my-products', UserProductsPageView.as_view(), name='product-user'),
    path('product/edit/<int:pk>/', EditProductView.as_view(), name='product-edit'),
    path('product/<int:pk>/delete-image/<int:img_id>/', DeleteImageView.as_view(), name='product-image-delete'),
    path('product/delete/<int:pk>/', DeleteProductView.as_view(), name='product-delete'),
    path('products/cart', CartUserView.as_view(), name='user-cart'),
    path('products/cart/<int:pk>/', DeleteCartProductView.as_view(), name='product-cart-delete'),
    path('products/addd/', add_to_cart, name='add-to-cart'),
    path('products/quantity/', change_quantity, name='change-quantity'),
    path('product/review/<int:pk>/', review_product, name='product-review'),
]
