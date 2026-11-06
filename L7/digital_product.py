"""A digital product is a Product but does not support shipping."""

from product import Product
from validation import non_negative_number


class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size, transactions=None):
        super().__init__(product_id, name, price, stock, transactions)
        self.__download_size = non_negative_number(download_size, "Download size")

    @property
    def download_size(self):
        return self.__download_size

    def display_information(self):
        super().display_information()
        print(f"Download size: {self.download_size:g} MB")
        print(self.get_fulfilment_info())

    def get_fulfilment_info(self):
        return "Delivered digitally through a download."
