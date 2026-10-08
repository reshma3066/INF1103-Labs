"""Week 5: manage a list of product dictionaries and save it as JSON."""

import json
import math
from pathlib import Path


INVENTORY_FILE = Path(__file__).with_name("inventory.json")


def load_inventory(filename=INVENTORY_FILE):
    """Load product dictionaries; a missing file starts an empty inventory."""
    path = Path(filename)
    if not path.exists():
        print("inventory.json not found. Starting with an empty inventory.")
        return []

    print("inventory.json found.")
    with open(path, "r", encoding="utf-8") as file:
        inventory = json.load(file)

    if not isinstance(inventory, list):
        raise ValueError("Inventory must be a list of product dictionaries.")
    checked = []
    for product in inventory:
        if not isinstance(product, dict):
            raise ValueError("Each product must be a dictionary.")
        if not all(key in product for key in ("id", "name", "price", "stock")):
            raise ValueError("Each product needs id, name, price and stock.")
        if not isinstance(product["id"], str) or not isinstance(product["name"], str):
            raise ValueError("Product ID and name must be text.")
        if type(product["price"]) not in (int, float):
            raise ValueError("Product price must be a number.")
        add_product(checked, product["id"], product["name"],
                    product["price"], product["stock"])
        # Older JSON files without history begin with their current stock.
        history = product.get("transactions", [product["stock"]])
        if (not isinstance(history, list)
                or any(type(amount) is not int for amount in history)
                or sum(history) != product["stock"]):
            raise ValueError("Transaction amounts must be integers summing to stock.")
        checked[-1]["transactions"] = history

    print("Inventory loaded successfully.")
    return checked


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


def save_inventory(inventory, filename=INVENTORY_FILE):
    """Save all product details and transaction amounts as readable JSON."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(inventory, file, indent=4, allow_nan=False)
        file.write("\n")


def read_number(prompt, whole_number=False):
    """Keep asking until a valid, non-negative price or quantity is entered."""
    while True:
        try:
            text = input(prompt)
            value = int(text) if whole_number else float(text)
            if value < 0 or (not whole_number and not math.isfinite(value)):
                raise ValueError
            return value
        except ValueError:
            kind = "whole number" if whole_number else "finite number"
            print(f"Please enter a non-negative {kind}.")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    try:
        inventory = load_inventory()
    except (OSError, ValueError) as error:
        print(f"Unable to load inventory: {error}")
        print("Please fix inventory.json before restarting. File left unchanged.")
        return 1

    while True:
        print("\n----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("----------------------------")

        try:
            option = input("\nEnter option: ").strip()
            if option == "1":
                display_all(inventory)
            elif option == "2":
                print("\nAdd New Product")
                product_id = input("Product ID: ").strip()
                if not product_id:
                    raise ValueError("Product ID cannot be empty.")
                if search_product(inventory, product_id) is not None:
                    raise ValueError("A product with this ID already exists.")
                name = input("Product Name: ").strip()
                if not name:
                    raise ValueError("Product name cannot be empty.")
                price = read_number("Price: ")
                stock = read_number("Stock Quantity: ", whole_number=True)
                add_product(inventory, product_id, name, price, stock)
                print("\nProduct added successfully!")
            elif option == "3":
                print("\nUpdate Stock")
                product_id = input("Enter Product ID: ")
                product = search_product(inventory, product_id)
                if product is None:
                    print("\nProduct not found.")
                    continue
                print("\nProduct Found:")
                print(f"Name: {product['name']}")
                print(f"Current Stock: {product['stock']}")
                stock = read_number("\nNew Stock Quantity: ", whole_number=True)
                update_stock(inventory, product_id, stock)
                print("\nStock updated successfully!")
            elif option == "4":
                print("\nSearch Product")
                product = search_product(inventory, input("Enter Product ID: "))
                if product is None:
                    print("\nProduct not found.")
                    continue
                print("\nProduct Found")
                print("-" * 48)
                print(f"ID: {product['id']}")
                print(f"Name: {product['name']}")
                print(f"Price: ${product['price']:.2f}")
                print(f"Stock: {product['stock']}")
                print("-" * 48)
            elif option == "5":
                print("\nSaving inventory...")
                save_inventory(inventory)
                print("Inventory saved successfully to inventory.json.")
            elif option == "6":
                print("\nSaving inventory before exit...")
                save_inventory(inventory)
                print("Inventory saved successfully.")
                print("\nThank you for using Inventory Management System.")
                print("Program terminated.")
                return 0
            else:
                print("Invalid option. Please choose 1 to 6.")
        except ValueError as error:
            print(error)
        except OSError as error:
            print(f"Unable to save inventory: {error}. Please try saving again.")
        except (EOFError, KeyboardInterrupt):
            print("\nInput ended. Saving inventory before exit...")
            try:
                save_inventory(inventory)
            except OSError as error:
                print(f"Unable to save inventory: {error}")
                return 1
            print("Inventory saved successfully. Program terminated.")
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
