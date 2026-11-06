"""Lab 7 behaviour checks; all writes use temporary inventory files."""

import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from file_handling import load_inventory, save_inventory
from inventory import Inventory
from main import main
from physical_product import PhysicalProduct
from product import Product


class Lab7Tests(unittest.TestCase):
    def setUp(self):
        self.physical = PhysicalProduct(" p001 ", "Guitar", 250, 5, 3)
        self.digital = DigitalProduct("D001", "Tutorial", 19.9, 100, 250)
        self.inventory = Inventory()
        self.inventory.add_product(self.physical)
        self.inventory.add_product(self.digital)
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "inventory.json"

    def test_abstract_contracts(self):
        with self.assertRaises(TypeError):
            Product("X", "Generic", 1, 1)
        with self.assertRaises(TypeError):
            CanBeShipped()
        class IncompleteProduct(Product):
            pass
        with self.assertRaises(TypeError):
            IncompleteProduct("X", "Incomplete", 1, 1)
        self.assertIsInstance(self.physical, CanBeShipped)
        self.assertNotIsInstance(self.digital, CanBeShipped)
        self.assertFalse(hasattr(self.digital, "calculate_shipping_cost"))

    def test_display_and_fulfilment(self):
        output = io.StringIO()
        with redirect_stdout(output):
            self.inventory.display_all()
        for expected in ("ID: P001", "Price: $250.00 | Stock: 5", "Weight: 3 kg",
                         "ID: D001", "Download size: 250 MB", "Shipping cost: $15.00"):
            self.assertIn(expected, output.getvalue())
        self.assertIn("shipping", self.physical.get_fulfilment_info())
        self.assertIn("digitally", self.digital.get_fulfilment_info())

    def test_shipping_for_different_weights(self):
        for weight, cost in ((0, 0), (0.5, 2.5), (3, 15)):
            with self.subTest(weight=weight):
                self.assertEqual(PhysicalProduct("P", "Item", 1, 1, weight)
                                 .calculate_shipping_cost(), cost)

    def test_validation(self):
        for cls in (PhysicalProduct, DigitalProduct):
            for value in (-1, float("nan"), float("inf"), True, "3"):
                with self.subTest(cls=cls, value=value), self.assertRaises(ValueError):
                    cls("P", "Item", 1, 1, value)
            for price, stock in ((-1, 1), (float("inf"), 1), (1, -1), (1, 1.5)):
                with self.assertRaises(ValueError):
                    cls("P", "Item", price, stock, 1)
        with self.assertRaises(ValueError):
            self.physical.update_stock(-1)
        self.assertEqual(self.physical.get_stock(), 5)

    def test_inventory_and_encapsulation(self):
        self.assertIs(self.inventory.search_product(" p001 "), self.physical)
        self.assertIsNone(self.inventory.search_product("missing"))
        with self.assertRaises(ValueError):
            self.inventory.add_product(PhysicalProduct("P001", "Duplicate", 1, 1, 1))
        with self.assertRaises(ValueError):
            self.inventory.add_product({})
        with self.assertRaises(ValueError):
            self.inventory.update_stock("missing", 5)
        self.inventory.update_stock("p001", 2)
        self.assertEqual(self.physical.get_transactions(), [5, -3])
        self.physical.get_transactions().clear()
        self.inventory.get_products().clear()
        self.assertEqual(self.physical.get_stock(), 2)
        self.assertEqual(len(self.inventory.get_products()), 2)
        self.assertEqual(self.digital.get_stock(), 100)

    def test_roundtrip_in_new_python_process(self):
        self.physical.update_stock(2)
        save_inventory(self.inventory, self.path)
        loaded = load_inventory(self.path)
        self.assertIsInstance(loaded.search_product("P001"), PhysicalProduct)
        self.assertIsInstance(loaded.search_product("D001"), DigitalProduct)
        self.assertEqual(loaded.search_product("P001").weight, 3)
        self.assertEqual(loaded.search_product("D001").download_size, 250)
        self.assertEqual(loaded.search_product("P001").get_transactions(), [5, -3])
        result = subprocess.run(
            [sys.executable, "-c", "from file_handling import load_inventory; "
             "import sys; load_inventory(sys.argv[1]).display_all()", str(self.path)],
            cwd=Path(__file__).parent, capture_output=True, text=True, check=True)
        self.assertIn("Weight: 3 kg", result.stdout)
        self.assertIn("Download size: 250 MB", result.stdout)
        self.assertIn("Stock: 2", result.stdout)

    def test_invalid_files_are_not_overwritten(self):
        save_inventory(self.inventory, self.path)
        record = json.loads(self.path.read_text())[0]
        for contents in ("{broken", "{}", "[1]", "[{}]",
                         json.dumps([dict(record, type="unknown")]),
                         json.dumps([dict(record, transactions=None)]),
                         json.dumps([record, record])):
            self.path.write_text(contents)
            with self.subTest(contents=contents):
                with self.assertRaises(ValueError):
                    load_inventory(self.path)
                with redirect_stdout(io.StringIO()):
                    self.assertEqual(main(self.path), 1)
                self.assertEqual(self.path.read_text(), contents)

    def test_missing_file_starts_empty(self):
        self.assertEqual(load_inventory(self.path).get_products(), [])

    def test_menu_add_both_types_update_search_save_and_restart(self):
        answers = ["1", "2", "P001", "Guitar", "bad", "250", "5", "9", "1", "3",
                   "2", "D001", "Tutorial", "19.9", "100", "2", "250",
                   "3", "p001", "2", "4", "D001", "1", "5", "6"]
        output = io.StringIO()
        with patch("builtins.input", side_effect=answers), redirect_stdout(output):
            self.assertEqual(main(self.path), 0)
        self.assertIn("Product Found:", output.getvalue())
        self.assertIn("Please enter a non-negative finite number", output.getvalue())
        with patch("builtins.input", side_effect=["1", "6"]), redirect_stdout(output):
            self.assertEqual(main(self.path), 0)
        self.assertIn("Weight: 3 kg", output.getvalue())
        self.assertIn("Download size: 250 MB", output.getvalue())
        self.assertEqual(load_inventory(self.path).search_product("P001").get_stock(), 2)


if __name__ == "__main__":
    unittest.main()
