from django.views.generic import TemplateView, DetailView

from shop.models import Order
from shop.mixins import ExtraContextMixin


class OrdersView(ExtraContextMixin, TemplateView):
    template_name = 'shop/orders/orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class OrderDetailsView(ExtraContextMixin, DetailView):
    model = Order
    template_name = 'shop/orders/order_details.html'
