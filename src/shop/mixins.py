from unicodedata import decimal

from .models import Product
from .context_functions import get_cart_id, get_items_in_cart, get_main_images, summary_price, \
    cart_products_id


class ExtraContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.id

        cart_id = get_cart_id(user)

        context['main_images'] = get_main_images()
        context['products'] = Product.objects.all()

        context['sum_price'] = summary_price(cart_id)
        context['cart_products_id'] = cart_products_id(cart_id)
        context['cart_item'] = get_items_in_cart(cart_id).values()

        context['cart_count'] = get_items_in_cart(cart_id).count()

        return context
