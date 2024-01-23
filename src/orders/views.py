from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, DetailView

from .models import Order
from shop.mixins import ExtraContextMixin


class OrdersView(ExtraContextMixin, TemplateView):
    template_name = 'orders/orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class OrderDetailsView(ExtraContextMixin, DetailView):
    model = Order
    template_name = 'orders/order_details.html'


class ClientsOrderDetailsView(ExtraContextMixin, DetailView):
    model = Order
    template_name = "orders/clients_order_details.html"


class ClientsOrdersView(ExtraContextMixin, TemplateView):
    template_name = "orders/clients_orders.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["logged_user"] = self.request.user.id

        return context


class SendOrderStatus(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        operation = request.POST.get("operation")
        tracking = request.POST.get('tracking')

        delivery_status = order.delivery.filter(order_id=order.id)[0]
        if operation == "order_status" and order.reception_code == '':
            delivery_status.status = 'Sent'
            order.tracking_number = tracking
        elif order.reception_code != '':
            messages.warning(request, "The order has been received")

        delivery_status.save()
        order.save()

        return redirect("client-order-details", pk)


class ReceiveOrderStatus(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        operation = request.POST.get("operation")
        reception_code = request.POST.get('reception_code')

        delivery_status = order.delivery.get()
        if operation == "order_status":
            delivery_status.status = 'Delivered'
            order.reception_code = reception_code

        delivery_status.save()
        order.save()

        return redirect("order-details", pk)
