from product import Product
from order_line import OrderLine


class Order:
    """Composition: an Order creates and manages its own OrderLine objects."""

    def __init__(self, order_id: str) -> None:
        self.__order_id: str = str(order_id)
        self.order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def add_order_line(self, product: Product, quantity: int) -> None:
        # The Order creates the OrderLine itself, showing composition.
        line: OrderLine = OrderLine(product, quantity)
        self.order_lines.append(line)

    def calculate_total(self) -> float:
        total: float = 0.0
        for line in self.order_lines:
            total += line.calculate_subtotal()
        return total

    def display_order(self) -> None:
        print(f"\n--- Order {self.__order_id} ---")
        if not self.order_lines:
            print("This order has no items.")
            return
        for line in self.order_lines:
            product: Product = line.get_product()
            print(
                f"{product.get_name()} x {line.get_quantity()} "
                f"= ${line.calculate_subtotal():.2f}"
            )
        print(f"Order total: ${self.calculate_total():.2f}")
