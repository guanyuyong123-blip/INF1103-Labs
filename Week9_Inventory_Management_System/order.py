from product import Product
from order_line import OrderLine
from discount_strategy import DiscountStrategy
from no_discount import NoDiscount


class Order:

    def __init__(
        self,
        order_id: str,
        discount: DiscountStrategy = None
    ):
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

        if discount is None:
            self.discount = NoDiscount()
        else:
            self.discount = discount

    def get_order_id(self) -> str:
        return self.order_id

    def add_order_line(
        self,
        product: Product,
        quantity: int
    ) -> None:

        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.discount = discount

    def calculate_total(self) -> float:

        total = sum(
            line.calculate_subtotal()
            for line in self.order_lines
        )

        return self.discount.apply(total)

    def display_order(self) -> None:

        print(f"\nOrder ID: {self.order_id}")

        for line in self.order_lines:
            print(
                f"{line.get_product().get_name()} "
                f"x {line.get_quantity()} "
                f"= ${line.calculate_subtotal():.2f}"
            )

        print(f"Total: ${self.calculate_total():.2f}")