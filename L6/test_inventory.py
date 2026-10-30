"""Check the OOP inventory system without changing the real inventory file."""

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from file_handling import load_inventory, save_inventory
from inventory import Inventory
from main import main
from product import Product


class ProductTests(unittest.TestCase):
    def test_objects_have_independent_state_and_replace_stock(self):
        first = Product(" p001 ", " Laptop ", 1200, 15)
        second = Product("P002", "Mouse", 25.50, 40)
        first.update_stock(50)
        first.update_stock(12)

        self.assertEqual(first.get_product_id(), "P001")
        self.assertEqual(first.get_name(), "Laptop")
        self.assertEqual(first.get_stock(), 12)
        self.assertEqual(first.get_transactions(), [15, 35, -38])
        self.assertEqual(second.get_stock(), 40)
        self.assertEqual(second.get_transactions(), [40])

    def test_history_is_preserved_and_copied_in_both_directions(self):
        original_history = [15, -3, 8]
        product = Product("P001", "Laptop", 1200, 20, original_history)
        original_history.append(99)
        returned_history = product.get_transactions()
        returned_history.clear()

        self.assertEqual(product.get_transactions(), [15, -3, 8])
        product.update_stock(7)
        self.assertEqual(product.get_transactions(), [15, -3, 8, -13])
        self.assertEqual(sum(product.get_transactions()), product.get_stock())

    def test_invalid_prices_and_stock_are_rejected(self):
        for price in (-1, float("inf"), float("nan"), True, "12.50"):
            with self.subTest(price=price), self.assertRaises(ValueError):
                Product("P001", "Laptop", price, 15)
        for stock in (-1, 1.5, True, "15"):
            with self.subTest(stock=stock), self.assertRaises(ValueError):
                Product("P001", "Laptop", 1200, stock)

        product = Product("P001", "Laptop", 1200, 15)
        with self.assertRaises(ValueError):
            product.update_stock(-1)
        self.assertEqual(product.get_stock(), 15)
        self.assertEqual(product.get_transactions(), [15])

    def test_invalid_names_and_transaction_histories_are_rejected(self):
        for product_id, name in ((" ", "Laptop"), ("P001", ""), (1, "Laptop")):
            with self.subTest(product_id=product_id, name=name):
                with self.assertRaises(ValueError):
                    Product(product_id, name, 1200, 15)
        for history in ([14], [True], [15.0], "15"):
            with self.subTest(history=history), self.assertRaises(ValueError):
                Product("P001", "Laptop", 1200, 15, history)


class InventoryTests(unittest.TestCase):
    def test_lookup_duplicate_prevention_and_collection_copy(self):
        inventory = Inventory()
        product = Product("P001", "Laptop", 1200, 15)
        inventory.add_product(product)
        self.assertIs(inventory.search_product(" p001 "), product)
        self.assertIsNone(inventory.search_product("P999"))

        with self.assertRaises(ValueError):
            inventory.add_product(Product("p001", "Duplicate", 1, 1))
        with self.assertRaises(ValueError):
            inventory.add_product({"id": "P002"})
        inventory.get_products().clear()
        self.assertEqual(inventory.get_products(), [product])

    def test_stock_update_and_display(self):
        inventory = Inventory()
        product = Product("P002", "Mouse", 25.5, 40)
        inventory.add_product(product)
        inventory.update_stock("p002", 12)
        self.assertEqual(product.get_stock(), 12)
        self.assertEqual(product.get_transactions(), [40, -28])
        with self.assertRaises(ValueError):
            inventory.update_stock("P999", 10)

        output = io.StringIO()
        with redirect_stdout(output):
            inventory.display_all()
        self.assertIn("ID: P002 | Name: Mouse | Price: $25.50 | Stock: 12", output.getvalue())


class TemporaryInventoryTests(unittest.TestCase):
    """Give file and menu tests their own automatically removed directory."""

    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.filename = Path(directory.name) / "inventory.json"

    def load_quietly(self):
        with redirect_stdout(io.StringIO()):
            return load_inventory(self.filename)


class FileHandlingTests(TemporaryInventoryTests):
    def test_json_roundtrip_restores_objects_and_history(self):
        inventory = Inventory()
        product = Product("P001", "Laptop", 1200, 20, [15, -3, 8])
        inventory.add_product(product)
        inventory.update_stock("P001", 18)
        save_inventory(inventory, self.filename)
        records = json.loads(self.filename.read_text(encoding="utf-8"))
        self.assertEqual(records[0]["transactions"], [15, -3, 8, -2])

        restored = self.load_quietly()
        loaded_product = restored.search_product("P001")
        self.assertIsInstance(restored, Inventory)
        self.assertIsInstance(loaded_product, Product)
        self.assertIsNot(loaded_product, product)
        self.assertEqual(loaded_product.get_name(), "Laptop")
        self.assertEqual(loaded_product.get_price(), 1200.0)
        self.assertEqual(loaded_product.get_stock(), 18)
        self.assertEqual(loaded_product.get_transactions(), [15, -3, 8, -2])

    def test_missing_file_and_empty_list_start_empty(self):
        self.assertEqual(self.load_quietly().get_products(), [])
        self.assertFalse(self.filename.exists())
        self.filename.write_text("[]", encoding="utf-8")
        self.assertEqual(self.load_quietly().get_products(), [])

    def test_legacy_record_starts_history_from_current_stock(self):
        records = [{"id": "P001", "name": "Laptop", "price": 1200, "stock": 15}]
        self.filename.write_text(json.dumps(records), encoding="utf-8")
        product = self.load_quietly().search_product("P001")
        self.assertEqual(product.get_transactions(), [15])

    def test_malformed_files_are_rejected_without_overwriting(self):
        invalid_files = (
            "{broken JSON",
            "{}",
            '[{"id": "P001"}]',
            '[{"id":"P001","name":"Laptop","price":1200,"stock":15,"transactions":null}]',
        )
        for contents in invalid_files:
            with self.subTest(contents=contents):
                self.filename.write_text(contents, encoding="utf-8")
                with self.assertRaises(ValueError):
                    self.load_quietly()
                with patch("builtins.input") as user_input:
                    with redirect_stdout(io.StringIO()):
                        self.assertEqual(main(self.filename), 1)
                    user_input.assert_not_called()
                self.assertEqual(self.filename.read_text(encoding="utf-8"), contents)


class MenuTests(TemporaryInventoryTests):
    def test_all_six_options_and_saved_inventory_reload(self):
        answers = [
            "1",                              # Display the empty inventory.
            "2", "p001", "Laptop", "1200", "15",
            "1",                              # Display the added product.
            "3", "p001", "50",              # Replace stock with 50.
            "4", "P001",                     # Search for the product.
            "5", "6",                        # Save, then exit and save again.
        ]
        output = io.StringIO()
        with patch("builtins.input", side_effect=answers):
            with patch("main.save_inventory", wraps=save_inventory) as save:
                with redirect_stdout(output):
                    self.assertEqual(main(self.filename), 0)
                self.assertEqual(save.call_count, 2)

        product = self.load_quietly().search_product("P001")
        self.assertEqual(product.get_stock(), 50)
        self.assertEqual(product.get_transactions(), [15, 35])
        self.assertIn("Inventory is empty.", output.getvalue())
        self.assertIn("Product Found:", output.getvalue())
        self.assertIn("Price: $1200.00 | Stock: 50", output.getvalue())

    def test_invalid_input_recovers_and_still_saves(self):
        answers = [
            "9",                              # Invalid menu option.
            "2", "",                         # Blank ID.
            "2", "P002", "",               # Blank name.
            "2", "P002", "Mouse",
            "bad", "nan", "-1", "25.50",  # Invalid prices, then a valid one.
            "3.5", "-4", "8",              # Invalid stock, then valid stock.
            "2", "p002",                    # Duplicate ID.
            "3", "missing",                 # Unknown ID when updating.
            "4", "missing",                 # Unknown ID when searching.
            "6",
        ]
        output = io.StringIO()
        with patch("builtins.input", side_effect=answers):
            with redirect_stdout(output):
                self.assertEqual(main(self.filename), 0)

        inventory = self.load_quietly()
        self.assertEqual(len(inventory.get_products()), 1)
        product = inventory.search_product("P002")
        self.assertEqual(product.get_price(), 25.5)
        self.assertEqual(product.get_stock(), 8)
        self.assertIn("Invalid option.", output.getvalue())
        self.assertIn("Please enter a non-negative finite number.", output.getvalue())
        self.assertIn("Please enter a non-negative whole number.", output.getvalue())
        self.assertIn("A product with this ID already exists.", output.getvalue())


if __name__ == "__main__":
    unittest.main()
