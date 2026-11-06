# Lab 7 UML class diagram

```mermaid
classDiagram
    class Product {
        <<abstract>>
        -str __product_id
        -str __name
        -float __price
        -int __stock
        -list __transactions
        +__init__(product_id, name, price, stock, transactions)
        +get_product_id() str
        +get_name() str
        +get_price() float
        +get_stock() int
        +get_transactions() list
        +update_stock(quantity)
        +display_information()
        +get_fulfilment_info()* str
    }
    class CanBeShipped {
        <<interface>>
        +calculate_shipping_cost()* float
    }
    class PhysicalProduct {
        -float __weight
        +float SHIPPING_RATE_PER_KG
        +__init__(product_id, name, price, stock, weight, transactions)
        +weight float
        +display_information()
        +get_fulfilment_info() str
        +calculate_shipping_cost() float
    }
    class DigitalProduct {
        -float __download_size
        +__init__(product_id, name, price, stock, download_size, transactions)
        +download_size float
        +display_information()
        +get_fulfilment_info() str
    }
    class Inventory {
        -list __products
        +__init__()
        +add_product(product)
        +search_product(product_id) Product
        +update_stock(product_id, quantity)
        +display_all()
        +get_products() list
    }
    Product <|-- PhysicalProduct
    Product <|-- DigitalProduct
    CanBeShipped <|.. PhysicalProduct
    Inventory "0..*" --> "0..*" Product : manages
```

Solid lines with hollow triangles show inheritance; the dashed line with a hollow
triangle shows interface realisation. Italic methods (marked with `*` in Mermaid)
are abstract. `weight` and `download_size` are read-only properties.
Inventory holds references to Product objects; it delegates product behaviour.
The code permits a product object to be referenced by more than one Inventory.
