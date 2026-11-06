"""An interface describes a capability, without storing product data."""

from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        """Return the shipping cost for this object."""
        pass
