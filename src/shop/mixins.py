from typing import Dict, Any
from .models import Order
from products.models import Product
from .context_functions import (
    get_main_images,
    summary_price,
    get_orders,
    get_user_cart,
    get_user_address,
    get_wishlist,
)


class ExtraContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context = self.__get_authorized_user_additional_context(context)

        context["main_images"] = get_main_images()
        context["products"] = Product.objects.all()
        context['all_orders'] = list(Order.objects.all())

        return context

    def __get_authorized_user_additional_context(self, context) -> Dict[str, Any]:
        user = self.request.user.id
        context["logged_user"] = user

        context["sum_price"] = summary_price(user)
        context["user_address"] = get_user_address(user)

        context["user_orders"] = get_orders(user).order_by("-created_at")
        context["user_cart"] = get_user_cart(user)
        context['wishlist'] = get_wishlist(user)

        return context
