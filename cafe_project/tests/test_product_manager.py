import pytest
from cafe_project.product import ProductManager, Product
from pathlib import Path
import json
import shutil

class TestProductManager:
    def setup_method(self):
        # Define paths
        self.original_file = Path("cafe_project/data/products2.json")
        self.test_file = Path("cafe_project/data/test_products2.json")
        
        # Copy the original products2.json to test_products2.json
        shutil.copy(self.original_file, self.test_file)
        
        # Create a ProductManager instance with the test file
        self.manager = ProductManager()
        self.manager._json_file = self.test_file  # Use the test file for all operations

    def teardown_method(self):
        # Delete the test file after each test to clean up
        if self.test_file.exists():
            self.test_file.unlink()

    def test_create_product(self):
        # Test creating a new product
        product = Product(product_id=999, name="Banana", price=1.5)
        self.manager.create(product)
        
        # Read back the product to verify
        created_product = self.manager.read(999)
        assert created_product.product_id == 999
        assert created_product.name == "Banana"
        assert created_product.price == 1.5
        
        # Check that creating a product with an existing ID raises an error
        with pytest.raises(ValueError, match=r"Product with ID 999 already exists"):
            self.manager.create(product)  # Creating the same product again should raise an error

    def test_read_product(self):
        # Test reading an existing product
        product = self.manager.read(1)
        assert product.product_id == 1
        assert product.name == "Existing Product Name"  # Replace with actual data in products2.json
        assert product.price == 5.0  # Replace with actual data in products2.json

        # Test reading a non-existent product raises KeyError
        with pytest.raises(KeyError):
            self.manager.read(9999)

    def test_update_product(self):
        # Update the details of an existing product
        updated_product = Product(product_id=1, name="Updated Product", price=10.0)
        self.manager.update(updated_product)

        # Read back the product and verify updates
        product = self.manager.read(1)
        assert product.name == "Updated Product"
        assert product.price == 10.0

    def test_delete_product(self):
        # Delete an existing product
        self.manager.delete(1)

        # Verify the product has been deleted
        with pytest.raises(KeyError):
            self.manager.read(1)

    def test_list_products(self):
        # List all products and verify the output
        products = self.manager.list()
        # Update the following assertion according to the initial data in your products2.json
        assert len(products) == 3  # Adjust based on the number of entries in products2.json
