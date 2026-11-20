INF1103 LAB 8 - INVENTORY MANAGEMENT SYSTEM

FILES
- supplier.py: Supplier class (association with Product)
- product.py: abstract Product parent class, supplier reference, common stock behaviour
- can_be_shipped.py: abstract shipping interface
- physical_product.py: PhysicalProduct subclass
- digital_product.py: DigitalProduct subclass
- inventory.py: Inventory class (aggregation)
- order_line.py: OrderLine class
- order.py: Order class (composition)
- inventory_auditor.py: interactive Inventory Management System with JSON save/load
- test_lab8.py: relationship, polymorphism and LSP tests
- UML_Lab8.mmd: Mermaid UML class diagram
- Predict_First_Lab8.docx: Predict First notes template with completed example answers

REQUIREMENTS
Python 3.10 or newer is recommended because the code uses union type hints such as Product | None.

RUN THE SYSTEM
1. Open this folder in VS Code.
2. Open a terminal in this folder.
3. Run: python inventory_auditor.py

RUN THE TESTS
Run: python test_lab8.py

VIEW THE UML
Paste the contents of UML_Lab8.mmd into https://mermaid.live and export it as PNG or PDF if your lecturer requests an image/PDF.

NOTES
- The shipping rate in this example is $5.00 per kg. Change it if your earlier Lab 7 specification used a different rate.
- The inventory is saved in inventory.json in this folder.
- The JSON save/load code uses isinstance only to identify a product's concrete type during serialization. Inventory operations and polymorphic display do not use subclass checks.
