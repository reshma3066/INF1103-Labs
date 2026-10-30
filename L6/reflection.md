# Lab 6 reflection questions

1. **What is the difference between a class and an object?**

   A class is a blueprint that defines attributes and methods. An object is one instance of that class, with its own values. For example, `Product` is a class, while `Product("P001", "Laptop", 1200.00, 15)` creates a product object.

2. **Why is Product a suitable class for this system?**

   Each item in the inventory has the same kinds of information and behaviour: an ID, name, price and stock, plus operations to update stock and display information. A `Product` class keeps this related data and behaviour together and lets us create many different products.

3. **What data belongs inside a Product object?**

   A product stores its product ID, name, price and current stock quantity. This program also keeps a list of stock transactions so that the transaction history from the Week 5 system is preserved.

4. **Why should the Product class manage its own stock rather than the main program directly changing it?**

   `Product.update_stock()` controls the change in one place. It can check that the new stock quantity is valid, set the stock and record the difference in the transaction history. For example, changing stock from 15 to 12 records `-3`.

5. **What does encapsulation mean in your program?**

   The product's data and the methods that manage it are kept together. Attributes such as `__stock` are intended to be private, so other code reads data through getters and changes stock through `update_stock()`. Python uses name mangling for these double-underscore attributes; it does not make them completely inaccessible. The transaction getter returns a copy so that changing the returned list does not change the stored history.

6. **What is the responsibility of the Product class?**

   `Product` represents and manages one product. It stores the product's information, provides getters, updates its own stock and displays its own information. Menu input and JSON file handling belong elsewhere.

7. **What is the responsibility of the Inventory class?**

   `Inventory` manages a collection of `Product` objects. It adds products, finds products by ID and displays the collection. When asked to update a product's stock, it finds that product and delegates the change to the product's `update_stock()` method.

8. **How does separating these responsibilities demonstrate the Single Responsibility Principle?**

   Each part has one clear job: `Product` manages one product, `Inventory` manages the collection, the main program handles the menu and input, and the file-handling functions load and save JSON. A change to the menu or JSON format can therefore be made without adding unrelated work to `Product`.

9. **What information does the main program need to know about a Product?**

   The main program needs to know the constructor's required values: product ID, name, price and stock. It needs to know the public interface it uses, including how to create a product and pass it to `Inventory`. It asks `Inventory` to add, search, display or update products instead of changing private attributes directly.

10. **What information about the internal implementation of Product does the main program not need to know?**

    The main program does not need to know the private attribute names, Python's mangled names, or how stock changes and transaction history are stored internally. It only needs to use the public methods correctly. The internal implementation can change while those public methods keep the same behaviour.
