from django.urls import path

from .views import HomePageView, ProductCreateView, DetailPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('product/add/', ProductCreateView.as_view(), name='product-add'),
    path('product/details/<int:pk>/', DetailPageView.as_view(), name='product-detail'),
]
