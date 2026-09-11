inventory = 0
failed_entries = 0

while True:
        stock = input("Enter stock quantity(or type 'quit' to exit): ")
        #is.lower() takes all inputs in lowercase
        if stock.islower()  =='quit':
            break
        
        if not stock.isdigit():
            print("Invalid input. Please enter a valid number.")
            failed_entries += 1
            continue
        