def get_valid_input():
    stock = input("Enter stock quantity (or 'quit' to stop): ")

    if stock.lower() == "quit":
        return "quit"

    if not stock.isdigit():
        print("Error: Invalid input. Please enter a number.")
        return None

    stock = int(stock)

    if stock < 0:
        print("Error: Stock quantity cannot be negative.")
        return None

    return stock


def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total


def calculate_tax(amount):
    tax = amount * 0.10
    return tax


def generate_report(total_units, failed_attempts, deliveries_processed):
    print("\n--- Inventory Report ---")
    print("Total Units Processed:", total_units)
    print("Total Deliveries Processed:", deliveries_processed)
    print("Number of Failed/Rejected Entries:", failed_attempts)


# Initialize inventory and counters
inventory = 0
failed_entries = 0
deliveries_processed = 0

# Continuous loop
while True:

    stock = get_valid_input()

    # User wants to quit
    if stock == "quit":
        break

    # Invalid input
    if stock is None:
        failed_entries += 1
        continue

    # Process valid delivery
    inventory = process_delivery(inventory, stock)

    # Calculate tax for this delivery
    tax = calculate_tax(stock)

    # Update delivery counter
    deliveries_processed += 1

    print("Stock accepted.")
    print("Current inventory:", inventory)
    print("Tax for this delivery:", tax)

    # Overstock alert
    if inventory > 500:
        print("ALERT: Overstock! Inventory exceeds 500 units.")
        break

# Generate final report
generate_report(inventory, failed_entries, deliveries_processed)