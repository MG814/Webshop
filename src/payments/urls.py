from django.urls import path

from .views import notify_stripe_view, CreateCheckoutSessionView

urlpatterns = [
    path("webhook", notify_stripe_view, name="stripe-webhook"),
    path(
        "create-checkout-session/",
        CreateCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
]
