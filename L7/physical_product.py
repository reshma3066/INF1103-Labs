"""A physical product is a Product and supports shipping."""

from can_be_shipped import CanBeShipped
from product import Product
from validation import non_negative_number


class PhysicalProduct(Product, CanBeShipped):
    SHIPPING_RATE_PER_KG = 5.0

    def __init__(self, product_id, name, price, stock, weight, transactions=None):
        super().__init__(product_id, name, price, stock, transactions)
        self.__weight = non_negative_number(weight, "Weight")

    @property
    def weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.weight:g} kg")
        print(self.get_fulfilment_info())
        print(f"Shipping cost: ${self.calculate_shipping_cost():.2f}")

    def get_fulfilment_info(self):
        return "Requires physical shipping."

    def calculate_shipping_cost(self):
        return round(self.weight * self.SHIPPING_RATE_PER_KG, 2)
