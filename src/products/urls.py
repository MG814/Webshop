from django.urls import path

from .views import (
    ProductCreateView,
    DetailPageView,
    DeleteProductView,
    UserProductsPageView,
    EditProductView,
    DeleteImageView,
    DeleteWishlistProductView,
    ReviewProduct,
)

urlpatterns = [
    path('product/add/', ProductCreateView.as_view(), name='product-add'),
    path('product/details/<int:pk>/', DetailPageView.as_view(), name='product-detail'),
    path('product/my-products', UserProductsPageView.as_view(), name='product-user'),
    path('product/edit/<int:pk>/', EditProductView.as_view(), name='product-edit'),
    path('product/<int:pk>/delete-image/<int:img_id>/', DeleteImageView.as_view(), name='product-image-delete'),
    path('product/delete/<int:pk>/', DeleteProductView.as_view(), name='product-delete'),
    path('product/review/<int:pk>/', ReviewProduct.as_view(), name='product-review'),
    path(
        "wishlist/product/delete/<int:pk>/",
        DeleteWishlistProductView.as_view(),
        name="product-wishlist-delete",
    ),
]
