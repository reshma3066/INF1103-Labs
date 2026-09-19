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


def generate_report(total_units, failed_attempts):
    """Print the final inventory and rejected-entry summary."""
    print("Total Units Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)


def main():
    # Keep the program's changing state local to this function.
    inventory = 0
    failed_entries = 0

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

        if inventory > 500:
            print("Overstock Alert! Inventory exceeds 500 units.")
            break

    generate_report(inventory, failed_entries)


if __name__ == "__main__":
    main()
