#!/usr/bin/env python3
"""Sample code with coding standards violations."""

def process_data(data):
    """Process data with standards violations."""
    result = []
    for item in data:
        # Line too long violation (>79 characters when formatted)
        processed_item = {"id": item["id"], "name": item["name"], "description": item["description"], "category": item["category"], "price": item["price"]}
        result.append(processed_item)
    return result

def risky_operation():
    """Function with bare except clause."""
    try:
        value = fetch_data()
        return value
    except:  # Bare except violation (E722)
        return None

def calculate_average(numbers):
    """Calculate average with whitespace violations."""
    total = sum(numbers)
    count = len(numbers)

    average = total / count  # Blank line above contains whitespace (W293)
    return average
