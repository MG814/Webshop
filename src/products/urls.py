from django.urls import path

from .views import (
    ProductCreateView,
    DetailPageView,
    DeleteProductView,
    UserProductsPageView,
    EditProductView,
    DeleteImageView,
    DeleteWishlistProductView,
    ReviewProduct, WishlistView, AddToWishList,
)

urlpatterns = [
    path('products/add/', ProductCreateView.as_view(), name='product-add'),
    path('products/details/<int:pk>/', DetailPageView.as_view(), name='product-detail'),
    path('products/my-products', UserProductsPageView.as_view(), name='product-user'),
    path('products/edit/<int:pk>/', EditProductView.as_view(), name='product-edit'),
    path('products/<int:pk>/delete-image/<int:img_id>/', DeleteImageView.as_view(), name='product-image-delete'),
    path('products/delete/<int:pk>/', DeleteProductView.as_view(), name='product-delete'),
    path('products/review/<int:pk>/', ReviewProduct.as_view(), name='product-review'),

    path("wishlist/", WishlistView.as_view(), name="wishlist"),
    path("wishlist/product/add/<int:pk>/", AddToWishList.as_view(), name="wishlist-product-add"),
    path(
        "wishlist/product/delete/<int:pk>/",
        DeleteWishlistProductView.as_view(),
        name="wishlist-product-delete",
    ),
]
