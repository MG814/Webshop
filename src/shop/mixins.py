from unicodedata import decimal

from .models import ItemInCart, Cart, Image, Product


class ExtraContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.id
        id_list = []
        cart_id = Cart.objects.filter(user_id=user).values('id')[0].get('id')

        items_in_cart = ItemInCart.objects.filter(cart_id=cart_id)

        sum = decimal('0')

        images = Image.objects.all()
        context['main_images'] = images.distinct('product')
        context['products'] = Product.objects.all()

        for product_in_cart in items_in_cart:
            sum += (product_in_cart.product.price * product_in_cart.quantity)
            id_list.append(product_in_cart.product.id)

        context['sum_price'] = sum
        context['cart_products_id'] = id_list
        context['cart_item'] = ItemInCart.objects.filter(cart_id=cart_id).values()

        context['cart_count'] = items_in_cart.count()

        return context

