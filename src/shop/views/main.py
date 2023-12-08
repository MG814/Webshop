import random
from typing import List, Dict, Any

from django.views.generic import TemplateView

from shop.models import Product
from django.db.models import QuerySet
from shop.mixins import ExtraContextMixin


class HomePageView(ExtraContextMixin, TemplateView):
    template_name = "shop/index.html"

    def get_random_products(self, count: int = 3) -> QuerySet[Product] | List:
        products = Product.objects.values('id')

        if products.count() > 0:
            product_count = [product.get('id') for product in products]  # TODO product_count tylko z liczb, które istnieją jako id.
            random_indices = random.sample(product_count, count)
            return Product.objects.filter(id__in=random_indices)
        else:
            return []

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['rand_items'] = self.get_random_products()
        return context
