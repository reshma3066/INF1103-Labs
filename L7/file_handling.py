"""Translate typed JSON records into product objects and back."""

import json
from pathlib import Path

from digital_product import DigitalProduct
from inventory import Inventory
from physical_product import PhysicalProduct


INVENTORY_FILE = Path(__file__).with_name("inventory.json")


def load_inventory(filename=INVENTORY_FILE):
    inventory = Inventory()
    path = Path(filename)
    if not path.exists():
        print("Inventory file not found. Starting with an empty inventory.")
        return inventory
    with path.open(encoding="utf-8") as file:
        records = json.load(file)
    if not isinstance(records, list):
        raise ValueError("Inventory data must be a list of product records.")
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Each saved product must be a JSON object.")
        if not all(key in record for key in ("type", "id", "name", "price", "stock")):
            raise ValueError("Each product needs type, id, name, price and stock.")
        common = (record["id"], record["name"], record["price"], record["stock"])
        history = record.get("transactions", [record["stock"]])
        if not isinstance(history, list):
            raise ValueError("Transaction history must be a list.")
        if record["type"] == "physical" and "weight" in record:
            product = PhysicalProduct(*common, record["weight"], history)
        elif record["type"] == "digital" and "download_size" in record:
            product = DigitalProduct(*common, record["download_size"], history)
        else:
            raise ValueError("Unknown product type or missing weight/download_size.")
        inventory.add_product(product)
    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory, filename=INVENTORY_FILE):
    records = []
    for product in inventory.get_products():
        record = {
            "id": product.get_product_id(), "name": product.get_name(),
            "price": product.get_price(), "stock": product.get_stock(),
            "transactions": product.get_transactions(),
        }
        if isinstance(product, PhysicalProduct):
            record.update(type="physical", weight=product.weight)
        elif isinstance(product, DigitalProduct):
            record.update(type="digital", download_size=product.download_size)
        else:
            raise ValueError("Unsupported product type; inventory was not saved.")
        records.append(record)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=4, allow_nan=False)
        file.write("\n")
