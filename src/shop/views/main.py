import random

from django.views.generic import TemplateView

from shop.models import Product
from shop.mixins import ExtraContextMixin


class HomePageView(ExtraContextMixin, TemplateView):
    template_name = "shop/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = list(Product.objects.all())
        if len(items) >= 3:
            random_items = random.sample(items, 3)
            context['rand_items'] = random_items

        return context
