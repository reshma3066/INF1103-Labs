"""A Product stores and manages the information for one inventory item."""

import math


class Product:
    """Keep product details private and change stock through a public method."""

    def __init__(self, product_id, name, price, stock, transactions=None):
        if not isinstance(product_id, str) or not isinstance(name, str):
            raise ValueError("Product ID and name must be text.")
        product_id = product_id.strip().upper()
        name = name.strip()
        if not product_id or not name:
            raise ValueError("Product ID and name cannot be empty.")
        if type(price) not in (int, float):
            raise ValueError("Price must be a finite, non-negative number.")
        try:
            price = float(price)
        except OverflowError:
            raise ValueError("Price must be a finite, non-negative number.")
        if not math.isfinite(price) or price < 0:
            raise ValueError("Price must be a finite, non-negative number.")
        if type(stock) is not int or stock < 0:
            raise ValueError("Stock must be a non-negative whole number.")

        # Older inventory files have no history, so start from their current stock.
        if transactions is None:
            transactions = [stock]
        if (not isinstance(transactions, list)
                or any(type(amount) is not int for amount in transactions)
                or sum(transactions) != stock):
            raise ValueError("Transaction amounts must be integers summing to stock.")

        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock
        self.__transactions = transactions.copy()

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def get_transactions(self):
        """Return a copy so callers cannot change the product's history directly."""
        return self.__transactions.copy()

    def update_stock(self, quantity):
        """Set a new stock quantity and record the signed change in units."""
        if type(quantity) is not int or quantity < 0:
            raise ValueError("Stock must be a non-negative whole number.")
        self.__transactions.append(quantity - self.__stock)
        self.__stock = quantity

    def display_information(self):
        """Display the details of this product."""
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )
