from django.urls import path

from .views.main import HomePageView
from .views.cart import CartUserView, DeleteCartProductView, AddToCart, ChangeQuantity

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),

    path('cart/', CartUserView.as_view(), name='user-cart'),
    path('cart/product/delete/<int:pk>/', DeleteCartProductView.as_view(), name='product-cart-delete'),
    path('cart/product/add/', AddToCart.as_view(), name='add-to-cart'),
    path('cart/product/quantity/', ChangeQuantity.as_view(), name='change-quantity'),
]
