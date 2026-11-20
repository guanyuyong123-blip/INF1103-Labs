from product import Product


class Inventory:
    """Aggregation: Inventory stores references to independently created Products."""

    def __init__(self) -> None:
        self.products: list[Product] = []

    def add_product(self, product: Product) -> None:
        if self.find_product(product.get_product_id()) is not None:
            raise ValueError("A product with this ID already exists in the inventory.")
        self.products.append(product)

    def remove_product(self, product_id: str) -> Product | None:
        """Remove and return a product; the Product object itself still exists."""
        product: Product | None = self.find_product(product_id)
        if product is not None:
            self.products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        for product in self.products:
            if product.get_product_id().lower() == str(product_id).lower():
                return product
        return None

    # Kept as an alias to support the earlier Lab 6/7 menu terminology.
    def search_product(self, search: str) -> Product | None:
        search_lower: str = str(search).lower()
        for product in self.products:
            if (
                product.get_product_id().lower() == search_lower
                or product.get_name().lower() == search_lower
            ):
                return product
        return None

    def display_all(self) -> None:
        print("\n--- Current Inventory ---")
        if not self.products:
            print("Inventory is empty.")
            return

        total_value: float = 0.0
        for product in self.products:
            product.display_information()
            print("Fulfilment:", product.get_fulfilment_info())
            print("-" * 60)
            total_value += product.get_price() * product.get_stock()

        print(f"Total Inventory Value: ${total_value:.2f}")

    def get_products(self) -> list[Product]:
        return self.products
