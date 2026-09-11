inventory = 0
failed_entries = 0

while True:
        stock = input("Enter stock quantity(or type 'quit' to exit): ")
        #is.lower() takes all inputs in lowercase
        if stock =='quit':
            break
        
        #validate non numeric input
        #is.digit already rejects negative numbers
        if not stock.isdigit():
            print("Invalid input. Please enter a valid number.")
            failed_entries += 1
            continue
        
        #Convert input to integer
        quantity = int(stock)
        
        #Add to inventory
        inventory += quantity
        
        