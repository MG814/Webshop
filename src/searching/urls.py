from django.urls import path

from .views import ElasticsearchView

urlpatterns = [
    path('search/', ElasticsearchView.as_view(), name='search'),
]
