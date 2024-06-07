from django.urls import path

from .views.main import HomePageView
from .views.cart import CartUserView, DeleteCartProductView, AddToCart, ChangeQuantity

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),

    path('cart/', CartUserView.as_view(), name='cart'),
    path('cart/products/<int:pk>/delete/', DeleteCartProductView.as_view(), name='cart-product-delete'),
    path('cart/products/<int:pk>/add/', AddToCart.as_view(), name='cart-product-add'),
    path('cart/products/quantity/', ChangeQuantity.as_view(), name='cart-product-quantity-change'),
]
