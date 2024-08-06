import random
from typing import List, Dict, Any

from django.views.generic import TemplateView

from shop.models import Product
from django.db.models import QuerySet
from shop.mixins import ExtraContextMixin


class HomePageView(ExtraContextMixin, TemplateView):
    template_name = "shop/index.html"

    def get_random_products(self, count: int = 3) -> QuerySet[Product] | List:
        products = Product.objects.values("id")

        if products.count() >= 3:
            product_count = [
                product.get("id") for product in products
            ]
            random_indices = random.sample(product_count, count)
            return Product.objects.filter(id__in=random_indices)
        else:
            return []

    def get_sort_query(self):
        sort = self.request.GET.get("sort", "l2h")
        return sort

    def sort_item(self):
        sort_val = self.get_sort_query()
        if sort_val == "l2hp":
            product_sorted = Product.objects.all().order_by("price")
        elif sort_val == "h2lp":
            product_sorted = Product.objects.all().order_by("-price")
        elif sort_val == "l2hr":
            product_sorted = Product.objects.all().order_by("reviews")
        elif sort_val == "h2lr":
            product_sorted = Product.objects.all().order_by("-reviews")
        else:
            product_sorted = Product.objects.all()
        return product_sorted

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["rand_items"] = self.get_random_products()

        context["products"] = self.sort_item()
        return context

