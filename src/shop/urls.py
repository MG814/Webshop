from django.urls import path

from .views import HomePageView, ProductCreateView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('product/add/', ProductCreateView.as_view(), name='product-add'),
]
