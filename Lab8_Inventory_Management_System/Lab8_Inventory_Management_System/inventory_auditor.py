import json
from pathlib import Path

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order

DATA_FILE: Path = Path(__file__).with_name("inventory.json")


def create_product_from_data(data: dict) -> Product:
    """Rebuild a Product object from saved JSON data."""
    supplier_data: dict = data["supplier"]
    supplier: Supplier = Supplier(
        supplier_data["supplier_id"],
        supplier_data["name"],
        supplier_data["contact_email"]
    )

    common: dict = {
        "product_id": data["product_id"],
        "name": data["name"],
        "price": data["price"],
        "stock_quantity": data["stock_quantity"],
        "supplier": supplier
    }

    if data["product_type"] == "physical":
        return PhysicalProduct(**common, weight=data["weight"])
    if data["product_type"] == "digital":
        return DigitalProduct(**common, download_size=data["download_size"])
    raise ValueError(f"Unknown product type: {data['product_type']}")


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
    data: list[dict] = [product_to_data(p) for p in inventory.products]
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    print(f"Inventory saved to {DATA_FILE.name}.")


def load_inventory(inventory: Inventory) -> None:
    if not DATA_FILE.exists():
        print("No saved inventory found. Starting with an empty inventory.")
        return

    with DATA_FILE.open("r", encoding="utf-8") as file:
        data: list[dict] = json.load(file)

    inventory.products.clear()
    for item in data:
        inventory.add_product(create_product_from_data(item))
    print(f"Loaded {len(inventory.products)} product(s).")


def add_new_product(inventory: Inventory) -> None:
    print("\n1. Physical product")
    print("2. Digital product")
    product_type: str = input("Choose product type: ").strip()

    product_id: str = input("Product ID: ").strip()
    name: str = input("Product name: ").strip()
    price: float = float(input("Price: $"))
    stock: int = int(input("Stock quantity: "))

    print("\nEnter supplier details (Supplier is created independently).")
    supplier_id: str = input("Supplier ID: ").strip()
    supplier_name: str = input("Supplier name: ").strip()
    supplier_email: str = input("Supplier email: ").strip()
    supplier: Supplier = Supplier(supplier_id, supplier_name, supplier_email)

    if product_type == "1":
        weight: float = float(input("Weight in kg: "))
        product: Product = PhysicalProduct(
            product_id, name, price, stock, supplier, weight
        )
    elif product_type == "2":
        download_size: float = float(input("Download size in MB: "))
        product = DigitalProduct(
            product_id, name, price, stock, supplier, download_size
        )
    else:
        print("Invalid product type.")
        return

    inventory.add_product(product)
    print("Product added successfully.")


def update_stock(inventory: Inventory) -> None:
    product_id: str = input("Enter product ID: ").strip()
    product: Product | None = inventory.find_product(product_id)
    if product is None:
        print("Product not found.")
        return

    quantity: int = int(input("Enter new stock quantity: "))
    try:
        product.update_stock(quantity)
        print("Stock updated.")
    except ValueError as error:
        print("Error:", error)


def search_product(inventory: Inventory) -> None:
    search: str = input("Enter product ID or name: ").strip()
    product: Product | None = inventory.search_product(search)
    if product is None:
        print("Product not found.")
    else:
        product.display_information()
        print("Fulfilment:", product.get_fulfilment_info())


def remove_product(inventory: Inventory) -> None:
    product_id: str = input("Enter product ID to remove: ").strip()
    removed: Product | None = inventory.remove_product(product_id)
    if removed is None:
        print("Product not found.")
    else:
        print("Product removed from this inventory. The Product object still exists.")
        removed.display_information()


def create_order(inventory: Inventory) -> None:
    order_id: str = input("Enter order ID: ").strip()
    order: Order = Order(order_id)

    while True:
        product_id: str = input("Enter product ID (or press Enter to finish): ").strip()
        if not product_id:
            break
        product: Product | None = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue
        try:
            quantity: int = int(input("Quantity: "))
            if quantity > product.get_stock():
                print("Not enough stock.")
                continue
            order.add_order_line(product, quantity)
            product.update_stock(product.get_stock() - quantity)
            print("Item added to order.")
        except ValueError as error:
            print("Invalid quantity:", error)

    order.display_order()


def main() -> None:
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
        print("8. Exit")

        choice: str = input("Enter your choice (1-8): ").strip()

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
                save_inventory(inventory)
                print("Thank you for using the Inventory Management System.")
                break
            else:
                print("Invalid choice. Please select 1-8.")
        except ValueError as error:
            print("Invalid input:", error)


if __name__ == "__main__":
    main()
