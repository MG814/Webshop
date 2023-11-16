from django.views.generic import TemplateView, DetailView

from shop.models import Item, Order
from shop.mixins import ExtraContextMixin


class OrdersView(ExtraContextMixin, TemplateView):
    template_name = 'shop/orders/orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.id

        user_orders = Order.objects.filter(user_id=user)

        context['orders'] = user_orders

        return context


class OrderDetailsView(ExtraContextMixin, DetailView):
    model = Item
    template_name = 'shop/orders/order_details.html'