from product import Product
from supplier import Supplier
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        weight: float
    ) -> None:
        super().__init__(product_id, name, price, stock_quantity, supplier)
        self.__weight: float = float(weight)

    def get_weight(self) -> float:
        return self.__weight

    def calculate_shipping_cost(self) -> float:
        # Example rate: $5.00 per kg.
        return self.__weight * 5.00

    def get_fulfilment_info(self) -> str:
        return (
            f"Physical item: ship to customer "
            f"(weight: {self.__weight:.2f} kg; "
            f"shipping: ${self.calculate_shipping_cost():.2f})"
        )

    def display_information(self) -> None:
        super().display_information()
        print(f"Type: Physical | Weight: {self.__weight:.2f} kg")
