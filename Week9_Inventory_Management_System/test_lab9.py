
import unittest

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order

from no_discount import NoDiscount
from percentage_discount import PercentageDiscount
from bulk_discount import BulkDiscount
from student_discount import StudentDiscount

from product_factory import ProductFactory


class TestLab9(unittest.TestCase):

    def setUp(self):
        self.supplier = Supplier(
            "S001",
            "ABC Supplies",
            "abc@example.com"
        )

        self.physical = PhysicalProduct(
            "P001",
            "Wireless Mouse",
            25.50,
            10,
            self.supplier,
            0.25
        )

        self.digital = DigitalProduct(
            "D001",
            "Antivirus Licence",
            39.90,
            20,
            self.supplier,
            150.0
        )

    def test_no_discount(self):
        order = Order("ORD001", NoDiscount())
        order.add_order_line(self.physical, 2)

        self.assertAlmostEqual(
            order.calculate_total(), 51.00
        )

    def test_percentage_discount(self):
        order = Order(
            "ORD002",
            PercentageDiscount(10)
        )

        order.add_order_line(self.physical, 2)

        self.assertAlmostEqual(
            order.calculate_total(), 45.90
        )

    def test_bulk_discount(self):
        order = Order(
            "ORD003",
            BulkDiscount(200, 20)
        )

        order.add_order_line(self.physical, 10)

        self.assertAlmostEqual(
            order.calculate_total(), 235.00
        )

    def test_change_discount(self):
        order = Order(
            "ORD004",
            BulkDiscount(200, 20)
        )

        order.add_order_line(self.physical, 10)

        order.set_discount(PercentageDiscount(10))

        self.assertAlmostEqual(
            order.calculate_total(), 229.50
        )

    def test_new_student_discount(self):
        order = Order(
            "ORD005",
            StudentDiscount()
        )

        order.add_order_line(self.physical, 2)

        self.assertAlmostEqual(
            order.calculate_total(), 48.45
        )

    def test_factory_physical(self):
        product = ProductFactory.create(
            "physical",
            "P002",
            "Desk Lamp",
            25.00,
            10,
            self.supplier,
            weight=1.0
        )

        self.assertIsInstance(product, PhysicalProduct)
        self.assertIsInstance(product, Product)

    def test_factory_digital(self):
        product = ProductFactory.create(
            "digital",
            "D002",
            "Software",
            50.00,
            20,
            self.supplier,
            download_size=100.0
        )

        self.assertIsInstance(product, DigitalProduct)
        self.assertIsInstance(product, Product)

    def test_unknown_product_type(self):
        with self.assertRaises(ValueError):
            ProductFactory.create(
                "service",
                "S003",
                "Installation",
                30.00,
                5,
                self.supplier
            )

    def test_invalid_price(self):
        with self.assertRaises(ValueError):
            PhysicalProduct(
                "P003",
                "Invalid Product",
                -10,
                5,
                self.supplier,
                0.5
            )

    def test_zero_price(self):
        with self.assertRaises(ValueError):
            PhysicalProduct(
                "P004",
                "Free Product",
                0,
                5,
                self.supplier,
                0.5
            )

    def test_negative_stock(self):
        with self.assertRaises(ValueError):
            DigitalProduct(
                "D003",
                "Invalid Software",
                20,
                -5,
                self.supplier,
                100
            )

    def test_invalid_order_quantity(self):
        with self.assertRaises(ValueError):
            order = Order("ORD006")
            order.add_order_line(self.physical, 0)

    def test_negative_order_quantity(self):
        with self.assertRaises(ValueError):
            order = Order("ORD007")
            order.add_order_line(self.physical, -2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
