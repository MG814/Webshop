from typing import Any


def get_shipping_options(
        shipping_name, shipping_price, max_day_shipping, min_day_shipping
) -> dict[str, dict[str, Any]]:
    return {
        "shipping_rate_data": {
            "type": "fixed_amount",
            "fixed_amount": {"amount": shipping_price * 100, "currency": "usd"},
            "display_name": shipping_name.replace("_", " "),
            "delivery_estimate": {
                "minimum": {"unit": "business_day", "value": min_day_shipping},
                "maximum": {"unit": "business_day", "value": max_day_shipping},
            },
        },
    }
