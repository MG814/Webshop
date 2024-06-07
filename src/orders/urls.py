from django.urls import path

from .views import (
    OrdersView,
    OrderDetailsView,
    ClientsOrdersView,
    ClientsOrderDetailsView,
    SendOrderStatus,
    ReceiveOrderStatus,
)

urlpatterns = [
    path('orders/', OrdersView.as_view(), name='order'),
    path('orders/<int:pk>/', OrderDetailsView.as_view(), name='order-details'),
    path("orders/clients", ClientsOrdersView.as_view(), name="order-client"),
    path("orders/<int:pk>/client", ClientsOrderDetailsView.as_view(), name="order-client-details"),
    path("orders/<int:pk>/send/", SendOrderStatus.as_view(), name="send"),
    path("orders/<int:pk>/recerive/", ReceiveOrderStatus.as_view(), name="receive"),
]
