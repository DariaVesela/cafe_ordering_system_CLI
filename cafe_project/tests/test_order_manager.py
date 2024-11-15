import pytest
from cafe_project.order import OrderManager, Order
from cafe_project.product import Product
from pathlib import Path
import json

class TestOrderManager:
    def setup_method(self):
        # Set up a temporary JSON file for testing
        self.test_file = Path("test_orders.json")
        self.manager = OrderManager()
        self.manager._json_file = self.test_file  # Use the test file instead of the real one
        # Create some test data
        self.test_data = {
            "1": {
                "date": 20231111,
                "time": 1400,
                "order_id": 1,
                "courier_id": 1,
                "products": [
                    {"product_id": 2, "name": "Cake", "price": 9.0}
                ],
                "progress": 1
            }
        }
        # Write initial data to test file
        self.test_file.write_text(json.dumps(self.test_data))

    def teardown_method(self):
        # Clean up the test file after each test
        if self.test_file.exists():
            self.test_file.unlink()

    def test_create_order(self):
        order = Order(date=20231112, time=1500, order_id=2, courier_id=2,
                      products=[Product(product_id=3, name="Pie", price=12.0)],
                      progress=1)
        self.manager.create(order)
        created_order = self.manager.read(2)
        
        assert created_order.order_id == 2
        assert created_order.date == 20231112
        assert created_order.products[0].name == "Pie"
        
        # Check that creating a duplicate raises an error
        with pytest.raises(ValueError):
            self.manager.create(order)

    def test_read_order(self):
        # Test reading an existing order
        order = self.manager.read(1)
        assert order.order_id == 1
        assert order.courier_id == 1

        # Test reading a non-existent order raises KeyError
        with pytest.raises(KeyError):
            self.manager.read(99)

    def test_update_order(self):
        # Update an existing order
        updated_order = Order(date=20231113, time=1600, order_id=1, courier_id=3,
                              products=[Product(product_id=4, name="Bread", price=7.0)],
                              progress=2)
        self.manager.update(updated_order)
        order = self.manager.read(1)
        
        assert order.courier_id == 3
        assert order.products[0].name == "Bread"
        assert order.progress == 2

    def test_delete_order(self):
        # Delete an existing order
        self.manager.delete(1)
        with pytest.raises(KeyError):
            self.manager.read(1)

        # Ensure deleting a non-existent order raises KeyError
        with pytest.raises(KeyError):
            self.manager.delete(99)

    def test_list_orders(self):
        # Test listing orders
        orders = self.manager.list()
        assert len(orders) == 1
        assert orders[0].order_id == 1
        assert orders[0].products[0].name == "Cake"
