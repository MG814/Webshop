from django.urls import path

from .views.main import HomePageView
from .views.cart import CartUserView, DeleteCartProductView, add_to_cart, change_quantity

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),

    path('cart/', CartUserView.as_view(), name='user-cart'),
    path('cart/product/delete/<int:pk>/', DeleteCartProductView.as_view(), name='product-cart-delete'),
    path('cart/product/add/', add_to_cart, name='add-to-cart'),
    path('cart/product/quantity/', change_quantity, name='change-quantity'),
]
