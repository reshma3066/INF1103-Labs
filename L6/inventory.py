"""An Inventory manages a collection of Product objects."""

from product import Product


class Inventory:
    """Add, find, update and display products without handling input or files."""

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        """Add a Product only when its ID is not already in the inventory."""
        if not isinstance(product, Product):
            raise ValueError("Inventory items must be Product objects.")
        if self.search_product(product.get_product_id()) is not None:
            raise ValueError("A product with this ID already exists.")
        self.__products.append(product)

    def search_product(self, product_id):
        """Find an ID without regard to letter case, or return None."""
        if not isinstance(product_id, str):
            raise ValueError("Product ID must be text.")
        product_id = product_id.strip().upper()
        for product in self.__products:
            if product.get_product_id().casefold() == product_id.casefold():
                return product
        return None

    def update_stock(self, product_id, quantity):
        """Find a product and let it manage its own stock change."""
        product = self.search_product(product_id)
        if product is None:
            raise ValueError("Product not found.")
        product.update_stock(quantity)

    def display_all(self):
        """Ask each product to display its own details."""
        print("\nCurrent Inventory")
        print("-" * 48)
        if not self.__products:
            print("Inventory is empty.")
        for product in self.__products:
            product.display_information()
        print("-" * 48)

    def get_products(self):
        """Return a list copy to protect the inventory's collection."""
        return self.__products.copy()
