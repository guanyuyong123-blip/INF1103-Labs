from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface-like abstract class for products that can be shipped."""

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass
