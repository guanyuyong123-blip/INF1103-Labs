inventory = 0
failed_entries = 0

while True:
    stock = input("Enter stock quantity (or 'quit' to stop): ")

    # User wants to quit
    if stock.lower() == "quit":
        break

    # Check if input is a valid number
    if not stock.isdigit():
        print("Error: Invalid input. Please enter a number.")
        failed_entries += 1
        continue

    # Convert the input from string to integer
    stock = int(stock)

    # Reject negative numbers
    if stock < 0:
        print("Error: Stock quantity cannot be negative.")
        failed_entries += 1
        continue

    # Add stock to inventory
    inventory += stock
    print("Stock accepted. Current inventory:", inventory)

    # Overstock alert
    if inventory > 500:
        print("ALERT: Overstock! Inventory exceeds 500 units.")
        break

print("\n--- Inventory Report ---")
print("Total Units Processed:", inventory)
print("Number of Failed/Rejected Entries:", failed_entries)