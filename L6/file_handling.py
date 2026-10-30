"""Load and save inventory data without putting file work in the classes."""

import json
from pathlib import Path

from inventory import Inventory
from product import Product


INVENTORY_FILE = Path(__file__).with_name("inventory.json")


def load_inventory(filename=INVENTORY_FILE):
    """Build Product objects from JSON; a missing file starts empty."""
    inventory = Inventory()
    path = Path(filename)
    if not path.exists():
        print("inventory.json not found. Starting with an empty inventory.")
        return inventory

    with open(path, "r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list):
        raise ValueError("Inventory data must be a list of product records.")

    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Each saved product must be a JSON object.")
        if not all(key in record for key in ("id", "name", "price", "stock")):
            raise ValueError("Each product needs id, name, price and stock.")
        history = record.get("transactions", [record["stock"]])
        if not isinstance(history, list):
            raise ValueError("Transaction history must be a list.")
        product = Product(
            record["id"], record["name"], record["price"], record["stock"],
            history,
        )
        inventory.add_product(product)

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory, filename=INVENTORY_FILE):
    """Convert objects to JSON records using their public methods."""
    records = []
    for product in inventory.get_products():
        records.append({
            "id": product.get_product_id(),
            "name": product.get_name(),
            "price": product.get_price(),
            "stock": product.get_stock(),
            "transactions": product.get_transactions(),
        })

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=4, allow_nan=False)
        file.write("\n")
