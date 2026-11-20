"""Run with: python test_lab8.py"""

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order


def show_product_details(product: Product) -> None:
    """One function works with every Product subclass (LSP + polymorphism)."""
    product.display_information()
    print("Fulfilment:", product.get_fulfilment_info())
    print()


def run_tests() -> None:
    print("TEST 1: Association - Supplier and Product")
    supplier: Supplier = Supplier("S001", "ABC Supplies", "abc@example.com")
    physical: PhysicalProduct = PhysicalProduct(
        "P001", "Wireless Mouse", 25.50, 10, supplier, 0.25
    )
    digital: DigitalProduct = DigitalProduct(
        "D001", "Antivirus Licence", 39.90, 20, supplier, 150.0
    )

    # Delete the local variable. Products retain their own references to Supplier.
    del supplier
    physical.display_supplier_information()
    digital.display_supplier_information()
    assert physical.get_supplier() is digital.get_supplier()
    print("PASS: Both products can still access the same Supplier object.\n")

    print("TEST 2: Aggregation - Products can move between inventories")
    inventory_a: Inventory = Inventory()
    inventory_b: Inventory = Inventory()
    inventory_a.add_product(physical)
    inventory_a.add_product(digital)

    moved_product: Product | None = inventory_a.remove_product("P001")
    assert moved_product is physical
    assert inventory_a.find_product("P001") is None
    inventory_b.add_product(moved_product)
    assert inventory_b.find_product("P001") is physical
    print("PASS: Removing a product did not destroy it; it was added to another Inventory.\n")

    print("TEST 3: Polymorphism - one Product collection")
    inventory_a.display_all()
    inventory_b.display_all()
    print("Calling the same function with both subclasses:")
    show_product_details(physical)
    show_product_details(digital)

    print("TEST 4: LSP - both subclasses preserve update_stock()")
    physical.update_stock(7)
    digital.update_stock(15)
    assert physical.get_stock() == 7
    assert digital.get_stock() == 15
    try:
        digital.update_stock(-1)
        raise AssertionError("Negative stock should have been rejected.")
    except ValueError:
        pass
    print("PASS: Both subclasses support the Product stock contract.\n")

    print("TEST 5: Composition - Order creates OrderLine objects")
    order: Order = Order("ORD001")
    order.add_order_line(physical, 2)
    order.add_order_line(digital, 1)
    assert len(order.order_lines) == 2
    expected_total: float = (physical.get_price() * 2) + digital.get_price()
    assert abs(order.calculate_total() - expected_total) < 0.001
    order.display_order()
    print("PASS: Order created its own lines and calculated the total.\n")

    print("ALL LAB 8 TESTS PASSED.")


if __name__ == "__main__":
    run_tests()
