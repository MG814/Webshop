from .models import Product
from .context_functions import get_main_images, summary_price, get_orders, get_user_cart, get_user_address


class ExtraContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.id

        context['main_images'] = get_main_images()
        context['products'] = Product.objects.all()

        context['sum_price'] = summary_price(user)
        context['user_address'] = get_user_address(user)

        context['user_orders'] = get_orders(user)
        context['user_cart'] = get_user_cart(user)

        return context
