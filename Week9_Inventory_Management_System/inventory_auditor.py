
import json
from pathlib import Path

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order

from product_factory import ProductFactory
from product_loader import load_products
from user_input import get_positive_float

DATA_FILE: Path = Path(__file__).with_name("inventory.json")


def create_product_from_data(data: dict) -> Product:
    """Rebuild a Product object using ProductFactory."""

    supplier_data: dict = data["supplier"]

    supplier: Supplier = Supplier(
        supplier_data["supplier_id"],
        supplier_data["name"],
        supplier_data["contact_email"]
    )

    return ProductFactory.create(
        data["product_type"],
        data["product_id"],
        data["name"],
        float(data["price"]),
        int(data["stock_quantity"]),
        supplier,
        weight=float(data.get("weight", 0.0)),
        download_size=float(data.get("download_size", 0.0))
    )


def product_to_data(product: Product) -> dict:
    """Convert a Product object into JSON-compatible data."""

    supplier: Supplier = product.get_supplier()

    data: dict = {
        "product_id": product.get_product_id(),
        "name": product.get_name(),
        "price": product.get_price(),
        "stock_quantity": product.get_stock(),
        "supplier": {
            "supplier_id": supplier.get_supplier_id(),
            "name": supplier.get_name(),
            "contact_email": supplier.get_contact_email()
        }
    }

    if isinstance(product, PhysicalProduct):
        data["product_type"] = "physical"
        data["weight"] = product.get_weight()

    elif isinstance(product, DigitalProduct):
        data["product_type"] = "digital"
        data["download_size"] = product.get_download_size()

    else:
        raise TypeError("Unsupported Product subclass.")

    return data


def save_inventory(inventory: Inventory) -> None:
    """Save all inventory products into JSON."""

    try:
        data: list[dict] = [
            product_to_data(product)
            for product in inventory.products
        ]

        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print(f"Inventory saved to {DATA_FILE.name}.")

    except (OSError, TypeError, ValueError) as error:
        print("Unable to save inventory:", error)


def load_inventory(inventory: Inventory) -> None:
    """Load products from the saved JSON file."""

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data: list[dict] = json.load(file)

    except FileNotFoundError:
        print("No saved inventory found. Starting with an empty inventory.")
        return

    except json.JSONDecodeError:
        print("Invalid inventory file. Starting with an empty inventory.")
        return

    except OSError as error:
        print("Unable to read inventory:", error)
        return

    inventory.products.clear()

    for item in data:
        try:
            product = create_product_from_data(item)
            inventory.add_product(product)

        except (ValueError, KeyError, TypeError) as error:
            print("Skipped invalid product:", error)

    print(f"Loaded {len(inventory.products)} product(s).")


def add_new_product(inventory: Inventory) -> None:
    """Ask for product details and create it through ProductFactory."""

    print("\n1. Physical product")
    print("2. Digital product")

    product_type: str = input("Choose product type: ").strip()

    if product_type not in ("1", "2"):
        print("Invalid product type.")
        return

    product_id: str = input("Product ID: ").strip()
    name: str = input("Product name: ").strip()

    price: float = get_positive_float("Price: $")

    try:
        stock: int = int(input("Stock quantity: "))

        if stock < 0:
            raise ValueError("Stock quantity cannot be negative.")

        print("\nEnter supplier details.")

        supplier: Supplier = Supplier(
            input("Supplier ID: ").strip(),
            input("Supplier name: ").strip(),
            input("Supplier email: ").strip()
        )

        if product_type == "1":

            weight: float = float(input("Weight in kg: "))

            product: Product = ProductFactory.create(
                "physical",
                product_id,
                name,
                price,
                stock,
                supplier,
                weight=weight
            )

        else:

            download_size: float = float(
                input("Download size in MB: ")
            )

            product = ProductFactory.create(
                "digital",
                product_id,
                name,
                price,
                stock,
                supplier,
                download_size=download_size
            )

        inventory.add_product(product)

        print("Product added successfully.")

    except ValueError as error:
        print("Invalid input:", error)


def update_stock(inventory: Inventory) -> None:
    """Update the stock quantity of an existing product."""

    product_id: str = input("Enter product ID: ").strip()

    product: Product | None = inventory.find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    try:
        quantity: int = int(
            input("Enter new stock quantity: ")
        )

        product.update_stock(quantity)

        print("Stock updated.")

    except ValueError as error:
        print("Invalid stock quantity:", error)


def search_product(inventory: Inventory) -> None:
    """Search for a product using its ID or name."""

    search: str = input("Enter product ID or name: ").strip()

    product: Product | None = inventory.search_product(search)

    if product is None:
        print("Product not found.")

    else:
        product.display_information()
        print("Fulfilment:", product.get_fulfilment_info())


def remove_product(inventory: Inventory) -> None:
    """Remove a product from the inventory."""

    product_id: str = input("Enter product ID to remove: ").strip()

    removed: Product | None = inventory.remove_product(product_id)

    if removed is None:
        print("Product not found.")

    else:
        print("Product removed from this inventory.")
        print("The Product object still exists.")
        removed.display_information()


def create_order(inventory: Inventory) -> None:
    """Create a customer order using existing inventory products."""

    order_id: str = input("Enter order ID: ").strip()

    order: Order = Order(order_id)

    while True:

        product_id: str = input(
            "Enter product ID (or press Enter to finish): "
        ).strip()

        if not product_id:
            break

        product: Product | None = inventory.find_product(product_id)

        if product is None:
            print("Product not found.")
            continue

        try:
            quantity: int = int(input("Quantity: "))

            if quantity <= 0:
                raise ValueError(
                    "Order quantity must be greater than zero."
                )

            if quantity > product.get_stock():
                print("Not enough stock.")
                continue

            order.add_order_line(product, quantity)

            product.update_stock(
                product.get_stock() - quantity
            )

            print("Item added to order.")

        except ValueError as error:
            print("Invalid quantity:", error)

    order.display_order()


def main() -> None:
    """Main menu of the Inventory Management System."""

    inventory: Inventory = Inventory()

    load_inventory(inventory)

    while True:

        print("\n========== INVENTORY MANAGEMENT SYSTEM ==========")
        print("1. Display all products")
        print("2. Add a product")
        print("3. Update product stock")
        print("4. Search for a product")
        print("5. Remove a product")
        print("6. Create customer order")
        print("7. Save inventory")
        print("8. Load products from products.csv")
        print("9. Exit")

        choice: str = input("Enter your choice (1-9): ").strip()

        try:

            if choice == "1":
                inventory.display_all()

            elif choice == "2":
                add_new_product(inventory)

            elif choice == "3":
                update_stock(inventory)

            elif choice == "4":
                search_product(inventory)

            elif choice == "5":
                remove_product(inventory)

            elif choice == "6":
                create_order(inventory)

            elif choice == "7":
                save_inventory(inventory)

            elif choice == "8":

                supplier: Supplier = Supplier(
                    "S001",
                    "ABC Supplies",
                    "abc@example.com"
                )

                load_products(
                    "products.csv",
                    inventory,
                    supplier
                )

            elif choice == "9":

                save_inventory(inventory)

                print(
                    "Thank you for using the Inventory Management System."
                )

                break

            else:
                print("Invalid choice. Please select 1-9.")

        except (ValueError, TypeError) as error:
            print("Invalid input:", error)


if __name__ == "__main__":
    main()
