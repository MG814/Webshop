from decimal import Decimal
from typing import Any


def _create_line_items(items_in_cart: list['Item'], shipping_name: str, shipping_price: Decimal, buyer_id: int) -> \
        list[dict[str, Any]]:
    line_items = []

    for item_in_cart in items_in_cart:
        # img = item_in_cart.product.images.first() # TODO Uncomment after app are deployed on AWS or other provider.
        dct = {
            "price_data": {
                "currency": "usd",
                "unit_amount": int(
                    float(item_in_cart.product.price.amount) * 100.00
                ),
                "product_data": {
                    "name": item_in_cart.product.title,
                    "metadata": {
                        "buyer_id": buyer_id,
                        "seller_id": item_in_cart.product.user.id,
                        "shipping_name": shipping_name.replace("_", " "),
                        "shipping_price": shipping_price,
                    },
                    # 'images': [img.image], # TODO Uncomment after app are deployed on AWS or other provider.
                },
            },
            "quantity": item_in_cart.quantity,
        }
        line_items.append(dct)
    return line_items
