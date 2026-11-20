import csv

from inventory import Inventory
from supplier import Supplier
from product_factory import ProductFactory


def load_products(
    path: str,
    inventory: Inventory,
    supplier: Supplier
) -> None:

    loaded = 0

    try:
        file = open(path, newline="", encoding="utf-8")

    except FileNotFoundError:
        print(f"Products file not found: {path}")

    else:
        with file:

            reader = csv.reader(file)

            # Skip the header row
            next(reader, None)

            for row_number, row in enumerate(reader, start=2):

                try:
                    product_type = row[0].strip()
                    product_id = row[1].strip()
                    name = row[2].strip()
                    price = float(row[3])
                    stock_quantity = int(row[4])

                    product = ProductFactory.create(
                        product_type,
                        product_id,
                        name,
                        price,
                        stock_quantity,
                        supplier
                    )

                    inventory.add_product(product)
                    loaded += 1

                except ValueError as error:
                    print(
                        f"Invalid row {row_number}: {error}"
                    )

                except IndexError:
                    print(
                        f"Invalid row {row_number}: "
                        "Missing data."
                    )

        print(f"{loaded} products loaded.")

    finally:
        print("Load attempt finished.")