inventory = 0
failed_entries = 0

while True:
    stock = input("Enter stock quantity (or type 'quit' to exit): ")

    if stock == "quit":
        break

    if not stock.isdigit():
        print("Invalid input. Please enter a valid number.")
        failed_entries += 1
        continue

    quantity = int(stock)
    inventory += quantity

    if inventory > 500:
        print("Overstock Alert! Inventory exceeds 500 units.")
        break

print("Total Units Processed:", inventory)
print("Number of Failed/Rejected Entries:", failed_entries)
        