from django.urls import path

from .views import HomePageView, ProductCreateView, DetailPageView, UserProductsPageView, EditProductView, \
    DeleteImageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('product/add/', ProductCreateView.as_view(), name='product-add'),
    path('product/details/<int:pk>/', DetailPageView.as_view(), name='product-detail'),
    path('product/my-products', UserProductsPageView.as_view(), name='product-user'),
    path('product/edit/<int:pk>/', EditProductView.as_view(), name='product-edit'),
    path('product/<int:pk>/delete-image/<int:img_id>/', DeleteImageView.as_view(), name='product-image-delete'),
]
