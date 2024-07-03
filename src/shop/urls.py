from django.urls import path

from shop.views.main import HomePageView
from shop.views.cart import CartUserView, DeleteCartProductView, AddToCart, ChangeQuantity, ActivateDiscountCode

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),

    path('cart/', CartUserView.as_view(), name='cart'),
    path('cart/products/<int:pk>/delete/', DeleteCartProductView.as_view(), name='cart-product-delete'),
    path('cart/products/<int:pk>/add/', AddToCart.as_view(), name='cart-product-add'),
    path('cart/products/quantity/', ChangeQuantity.as_view(), name='cart-product-quantity-change'),
    path('cart/activatecode', ActivateDiscountCode.as_view(), name='cart-activate-code'),
]
