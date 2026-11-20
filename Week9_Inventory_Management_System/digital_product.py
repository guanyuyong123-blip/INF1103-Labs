from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        download_size: float
    ) -> None:
        super().__init__(product_id, name, price, stock_quantity, supplier)
        self.__download_size: float = float(download_size)

    def get_download_size(self) -> float:
        return self.__download_size

    def get_fulfilment_info(self) -> str:
        return f"Digital download ({self.__download_size:.2f} MB); no physical shipping required"

    def display_information(self) -> None:
        super().display_information()
        print(f"Type: Digital | Download size: {self.__download_size:.2f} MB")
