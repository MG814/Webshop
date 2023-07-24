from django.urls import path
from django.views.generic import TemplateView

from src.shop.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]
