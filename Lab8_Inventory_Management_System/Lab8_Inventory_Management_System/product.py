from abc import ABC, abstractmethod
from supplier import Supplier


class Product(ABC):
    """Abstract parent class shared by physical and digital products."""

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier
    ) -> None:
        self.__product_id: str = str(product_id)
        self.__name: str = name
        self.__price: float = float(price)
        self.__stock_quantity: int = int(stock_quantity)
        # Association: Product keeps a reference to an independently created Supplier.
        self.__supplier: Supplier = supplier

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock_quantity

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def display_supplier_information(self) -> None:
        self.__supplier.display_information()

    def update_stock(self, quantity: int) -> None:
        """Set stock to a non-negative quantity; subclasses retain this behaviour."""
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.__stock_quantity = quantity

    def add_stock(self, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.__stock_quantity += quantity

    def display_information(self) -> None:
        total_value: float = self.__price * self.__stock_quantity
        print(
            f"ID: {self.__product_id} | Product: {self.__name} | "
            f"Price: ${self.__price:.2f} | Quantity: {self.__stock_quantity} | "
            f"Total: ${total_value:.2f}"
        )
        print(
            f"Supplier: {self.__supplier.get_name()} "
            f"({self.__supplier.get_supplier_id()})"
        )

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return the fulfilment method for this product."""
        pass
