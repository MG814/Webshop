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
    path('orders/', OrdersView.as_view(), name='orders'),
    path('orders/order/<int:pk>/', OrderDetailsView.as_view(), name='order-details'),
    path("orders/clients", ClientsOrdersView.as_view(), name="clients-orders"),
    path("orders/order/<int:pk>/client", ClientsOrderDetailsView.as_view(), name="client-order-details"),
    path("orders/send/<int:pk>/", SendOrderStatus.as_view(), name="send"),
    path("orders/recerive/<int:pk>/", ReceiveOrderStatus.as_view(), name="receive"),
]
