"""Week 5: manage a list of product dictionaries and save it as JSON."""

import math


def search_product(inventory, product_id):
    """Return the product with this ID, or None if it does not exist."""
    for product in inventory:
        if product["id"].casefold() == product_id.strip().casefold():
            return product
    return None


def add_product(inventory, product_id, name, price, stock):
    """Add a unique product, including its opening stock transaction."""
    product_id = product_id.strip().upper()
    name = name.strip()
    if not product_id or not name:
        raise ValueError("Product ID and name cannot be empty.")
    if search_product(inventory, product_id) is not None:
        raise ValueError("A product with this ID already exists.")
    if not math.isfinite(price) or price < 0:
        raise ValueError("Price must be a finite, non-negative number.")
    if type(stock) is not int or stock < 0:
        raise ValueError("Stock must be a non-negative whole number.")
    inventory.append({
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock,
        "transactions": [stock],
    })


def update_stock(inventory, product_id, new_stock):
    """Set the stock quantity and remember the signed change in units."""
    product = search_product(inventory, product_id)
    if product is None:
        raise ValueError("Product not found.")
    if type(new_stock) is not int or new_stock < 0:
        raise ValueError("Stock must be a non-negative whole number.")
    product["transactions"].append(new_stock - product["stock"])
    product["stock"] = new_stock


def display_all(inventory):
    """Display every product using the lab's sample format."""
    print("\nCurrent Inventory")
    print("-" * 48)
    if not inventory:
        print("Inventory is empty.")
    for product in inventory:
        print(
            f"ID: {product['id']} | Name: {product['name']} | "
            f"Price: ${product['price']:.2f} | Stock: {product['stock']}"
        )
    print("-" * 48)
