import stripe

from django.http import HttpResponse

from django.shortcuts import redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from decimal import Decimal

from shop.mixins import ExtraContextMixin
from shop.context_functions import get_user_cart

from payments.cart import _create_line_items
from payments.email_utils import send_email
from payments.orders import create_new_order, create_new_delivery, transfer_items_from_cart_to_order
from payments.shipping import get_shipping_options

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(ExtraContextMixin, View):
    def post(self, request, *args, **kwargs):
        user = self.request.user.id
        cart = get_user_cart(user)
        shipping_price = Decimal("0")
        min_day, max_day = 1, 1

        shipping = request.POST.get("shipping")
        if shipping == "Free":
            shipping_price = Decimal("0")
            min_day, max_day = 5, 7
        elif shipping == "Next_day_air":
            shipping_price = Decimal("15")
            min_day, max_day = 1, 1

        YOUR_DOMAIN = "http://127.0.0.1:8000"

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card", "paypal"],
            shipping_options=[
                get_shipping_options(shipping, shipping_price, max_day, min_day)
            ],
            line_items=_create_line_items(
                cart.items_in_cart.all(), shipping, shipping_price, user
            ),
            mode="payment",
            invoice_creation={"enabled": True},
            success_url=YOUR_DOMAIN + "/orders/",
            cancel_url=YOUR_DOMAIN + "",
        )
        print("+++++++++++++++++++++++++++++++++++")
        print(checkout_session.url)
        print("+++++++++++++++++++++++++++++++++++")
        return redirect(checkout_session.url, code=303)


@csrf_exempt
def notify_stripe_view(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.ENDPOINT_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event["data"]["object"]["id"],
            expand=["line_items"],
        )

        line_items = session.line_items
        price = line_items.get("data")[0].get("price")
        product = price.get("product")
        metadata = stripe.Product.retrieve(product).get("metadata")
        seller_id = metadata.get("seller_id")
        buyer_id = metadata.get("buyer_id")
        cart = get_user_cart(buyer_id)
        price_amount = metadata.get("shipping_price")

        order = create_new_order(buyer_id, seller_id, cart, price_amount)
        create_new_delivery(metadata.get("shipping_name"), price_amount, order.id)
        transfer_items_from_cart_to_order(cart, order)

    if event["type"] == 'charge.updated':
        charge = stripe.Charge.retrieve(
            event["data"]["object"]["id"],
        )
        buyer_email = stripe.Customer.list().get('data')[0].get('email')
        send_email(receipt_url=charge.get('receipt_url'), buyer_email=buyer_email)

    # Passed signature verification
    return HttpResponse(status=200)
