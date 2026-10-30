"""Week 8 Lab 6: menu for the object-oriented inventory system."""

import math

from file_handling import INVENTORY_FILE, load_inventory, save_inventory
from product import Product


def read_number(prompt, whole_number=False):
    """Ask again if the user enters an invalid price or stock quantity."""
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


def display_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main(filename=INVENTORY_FILE):
    print("=" * 40)
    print("OOP INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    try:
        inventory = load_inventory(filename)
    except (OSError, ValueError) as error:
        print(f"Unable to load inventory: {error}")
        print("Please fix inventory.json before restarting. File left unchanged.")
        return 1

    while True:
        display_menu()
        try:
            option = input("\nEnter option: ").strip()
            if option == "1":
                inventory.display_all()
            elif option == "2":
                print("\nAdd New Product")
                product_id = input("Product ID: ").strip()
                if not product_id:
                    raise ValueError("Product ID cannot be empty.")
                if inventory.search_product(product_id) is not None:
                    raise ValueError("A product with this ID already exists.")
                name = input("Product Name: ").strip()
                if not name:
                    raise ValueError("Product name cannot be empty.")
                price = read_number("Price: ")
                stock = read_number("Stock Quantity: ", whole_number=True)
                product = Product(product_id, name, price, stock)
                inventory.add_product(product)
                print("Product added successfully!")
            elif option == "3":
                print("\nUpdate Stock")
                product_id = input("Enter Product ID: ")
                product = inventory.search_product(product_id)
                if product is None:
                    print("Product not found.")
                    continue
                print(f"Name: {product.get_name()}")
                print(f"Current Stock: {product.get_stock()}")
                stock = read_number("New Stock Quantity: ", whole_number=True)
                inventory.update_stock(product_id, stock)
                print("Stock updated successfully!")
            elif option == "4":
                print("\nSearch Product")
                product = inventory.search_product(input("Enter Product ID: "))
                if product is None:
                    print("Product not found.")
                else:
                    print("Product Found:")
                    product.display_information()
            elif option == "5":
                save_inventory(inventory, filename)
                print("Inventory saved successfully to inventory.json.")
            elif option == "6":
                save_inventory(inventory, filename)
                print("Inventory saved successfully. Goodbye!")
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
                save_inventory(inventory, filename)
            except OSError as error:
                print(f"Unable to save inventory: {error}")
                return 1
            print("Inventory saved successfully. Goodbye!")
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
