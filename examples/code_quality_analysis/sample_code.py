#!/usr/bin/env python3
"""Sample code with quality issues for demonstration."""


def calculate_total(items, tax_rate, discount_code, is_member, country, currency):
    """Calculate order total with complex logic."""
    subtotal = 0
    for item in items:
        if item['active']:
            if item['on_sale']:
                if is_member:
                    if discount_code:
                        if country == 'US':
                            if currency == 'USD':
                                price = item['price'] * 0.7
                            else:
                                price = item['price'] * 0.75
                        else:
                            price = item['price'] * 0.8
                    else:
                        price = item['price'] * 0.9
                else:
                    price = item['price'] * 0.95
            else:
                price = item['price']
            subtotal += price * item['quantity']

    # TODO: Add international shipping calculation
    # FIXME: Tax calculation doesn't handle all states correctly

    tax = subtotal * tax_rate
    total = subtotal + tax

    return total


def process_order(order_id, customer_id, items, payment_method, shipping_address, billing_address, gift_message, gift_wrap, express_shipping, insurance, signature_required):
    """Process order with many parameters."""
    # HACK: Temporary fix for payment processing
    result = calculate_total(items, 0.08, None, False, 'US', 'USD')
    return result


class OrderManager:
    def __init__(self):
        pass

    def create_order(self):
        pass

    def update_order(self):
        pass

    def cancel_order(self):
        pass
