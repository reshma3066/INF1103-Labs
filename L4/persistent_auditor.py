from pathlib import Path


def load_inventory():
    """Read the saved total and transaction history, or start empty."""
    inventory_file = Path(__file__).with_name("inventory.txt")

    try:
        with open(inventory_file, "r", encoding="utf-8") as file:
            total = int(file.readline())
            history_line = file.readline().strip()

            history = []
            if history_line:
                for amount in history_line.split(","):
                    history.append(int(amount))

        return total, history
    except FileNotFoundError:
        return 0, []


def save_inventory(total, history):
    """Write the total and transaction history to inventory.txt."""
    inventory_file = Path(__file__).with_name("inventory.txt")

    with open(inventory_file, "w", encoding="utf-8") as file:
        file.write(f"{total}\n")
        file.write(",".join(str(amount) for amount in history) + "\n")


def get_valid_input():
    """Return a non-negative integer or 'quit'; reject other input."""
    stock = input("Enter stock quantity (or type 'quit' to exit): ")

    if stock == "quit":
        return "quit"

    # Unlike isdigit(), isdecimal() excludes characters such as superscripts.
    if not stock.isdecimal():
        raise ValueError("Invalid input. Please enter a valid number.")

    return int(stock)


def process_delivery(current_total, new_value):
    """Return the inventory total after adding one delivery."""
    return current_total + new_value


def calculate_tax(amount):
    """Return 10% of this delivery's amount."""
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    """Print the final inventory and rejected-entry summary."""
    print("Total Units Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)


def main():
    # Keep the program's changing state local to this function.
    inventory, transaction_history = load_inventory()
    failed_entries = 0
    deliveries_processed = 0

    print("Starting inventory:", inventory)
    print("Previous transactions:", transaction_history)

    while True:
        try:
            quantity = get_valid_input()
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            failed_entries += 1
            continue

        if quantity == "quit":
            break

        inventory = process_delivery(inventory, quantity)
        transaction_history.append(quantity)
        tax = calculate_tax(quantity)
        deliveries_processed += 1
        print(f"Tax for this delivery: {tax:.2f}")

        if inventory > 500:
            print("Overstock Alert! Inventory exceeds 500 units.")
            break

    save_inventory(inventory, transaction_history)
    print("Inventory saved to inventory.txt.")
    print("Transaction history:", transaction_history)
    print("Total Deliveries Processed:", deliveries_processed)
    generate_report(inventory, failed_entries)


if __name__ == "__main__":
    main()
