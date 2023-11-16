import stripe

from django.http import HttpResponse

from django.shortcuts import redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from django.conf import settings

from shop.models import Order, Delivery
from shop.mixins import ExtraContextMixin
from shop.context_functions import get_user_cart

stripe.api_key = settings.STRIPE_SECRET_KEY


def get_shipping_options(shipping_name, shipping_price, max_day_shipping, min_day_shipping):
    shipping_options = {
            'shipping_rate_data': {
                "type": "fixed_amount",
                "fixed_amount": {"amount": shipping_price * 100, "currency": "usd"},
                "display_name": shipping_name.replace('_', ' '),
                "delivery_estimate": {
                    "minimum": {"unit": "business_day", "value": min_day_shipping},
                    "maximum": {"unit": "business_day", "value": max_day_shipping},
                },
            },
        }
    return shipping_options


class CreateCheckoutSessionView(ExtraContextMixin, View):
    def _create_line_items(self, items_in_cart, shipping_name, shipping_price):
        line_items = []

        for item_in_cart in items_in_cart:
            # img = item_in_cart.product.images.first() # TODO Uncomment after app are deployed on AWS or other provider.
            dct = {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(float(item_in_cart.product.price.amount) * 100.00),
                    'product_data': {
                        'name': item_in_cart.product.title,
                        'metadata': {"user_id": item_in_cart.product.user.id,
                                     'shipping_name': shipping_name.replace('_', ' '),
                                     'shipping_price': shipping_price,
                                     },
                        # 'images': [img.image], # TODO Uncomment after app are deployed on AWS or other provider.
                    },
                },
                'quantity': item_in_cart.quantity,
            }
            line_items.append(dct)
        return line_items

    def post(self, request, *args, **kwargs):
        user = self.request.user.id
        cart = get_user_cart(user)
        shipping_price = Decimal('0')
        min_day, max_day = 1, 1

        shipping = request.POST.get('shipping')
        if shipping == 'Free':
            shipping_price = Decimal('0')
            min_day, max_day = 5, 7
        elif shipping == 'Next_day_air':
            shipping_price = Decimal('15')
            min_day, max_day = 1, 1

        YOUR_DOMAIN = "http://127.0.0.1:8000"

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card', 'paypal'],
            shipping_options=[get_shipping_options(shipping, shipping_price, max_day, min_day)],
            line_items=self._create_line_items(cart.items_in_cart.all(), shipping, shipping_price),
            mode='payment',
            success_url=YOUR_DOMAIN + '/orders/',  # TODO na potem reverse_lazy
            cancel_url=YOUR_DOMAIN + '',
        )
        print('+++++++++++++++++++++++++++++++++++')
        print(checkout_session.url)
        print('+++++++++++++++++++++++++++++++++++')
        return redirect(checkout_session.url, code=303)


@csrf_exempt
def notify_stripe_view(request):  # notify_stripe
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.ENDPOINT_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )

        line_items = session.line_items
        price = line_items.get('data')[0].get('price')
        product = price.get('product')
        metadata = stripe.Product.retrieve(product).get('metadata')
        user_id = metadata.get('user_id')
        cart = get_user_cart(user_id)

        price_amount = metadata.get('shipping_price')

        order = Order(user_id=user_id)
        order.price_with_shipping.amount = cart.total_price.amount + Decimal(price_amount)
        order.save()

        delivery = Delivery(name=metadata.get('shipping_name'), price=price_amount, order_id=order.id)
        delivery.save()

        for item_in_cart in cart.items_in_cart.all():
            item_in_cart.order = order
            item_in_cart.save()
            item_in_cart.cart = None
            item_in_cart.save()

    # Passed signature verification
    return HttpResponse(status=200)
