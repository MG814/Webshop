from django.urls import path

from .views.main import HomePageView

from .views.cart import CartUserView, DeleteCartProductView, add_to_cart, change_quantity
from .views.products import ProductCreateView, DetailPageView, DeleteProductView, UserProductsPageView, EditProductView, \
    DeleteImageView, review_product
from .views.orders import OrdersView, OrderDetailsView
from .views.stripe import notify_stripe_view, CreateCheckoutSessionView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),

    path('product/add/', ProductCreateView.as_view(), name='product-add'),
    path('product/details/<int:pk>/', DetailPageView.as_view(), name='product-detail'),
    path('product/my-products', UserProductsPageView.as_view(), name='product-user'),
    path('product/edit/<int:pk>/', EditProductView.as_view(), name='product-edit'),
    path('product/<int:pk>/delete-image/<int:img_id>/', DeleteImageView.as_view(), name='product-image-delete'),
    path('product/delete/<int:pk>/', DeleteProductView.as_view(), name='product-delete'),
    path('product/review/<int:pk>/', review_product, name='product-review'),

    path('cart/', CartUserView.as_view(), name='user-cart'),
    path('cart/product/delete/<int:pk>/', DeleteCartProductView.as_view(), name='product-cart-delete'),
    path('cart/product/add/', add_to_cart, name='add-to-cart'),
    path('cart/product/quantity/', change_quantity, name='change-quantity'),

    path('orders/', OrdersView.as_view(), name='orders'),
    path('orders/order/<int:pk>/', OrderDetailsView.as_view(), name='order-details'),

    path('webhook', notify_stripe_view, name='stripe-webhook'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
]
