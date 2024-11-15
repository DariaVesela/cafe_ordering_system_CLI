import pytest
from cafe_project.customer import CustomerManager, Customer
from pathlib import Path
import json
import shutil

class TestCustomerManager:
    def setup_method(self):
        # Define paths
        self.original_file = Path("cafe_project/data/customers.json")
        self.test_file = Path("cafe_project/data/test_customers.json")
        
        # Copy the original customers.json to test_customers.json
        shutil.copy(self.original_file, self.test_file)
        
        # Create a CustomerManager instance with the test file
        self.manager = CustomerManager()
        self.manager._json_file = self.test_file  # Use the test file for all operations

    def teardown_method(self):
        # Delete the test file after each test to clean up
        if self.test_file.exists():
            self.test_file.unlink()

    def test_create_customer(self):
        # Test creating a new customer
        customer = Customer(customer_id=999, name="John Doe", address="123 Main St", phone="0789789789")
        self.manager.create(customer)
        
        # Read back the customer to verify
        created_customer = self.manager.read(999)
        assert created_customer.customer_id == 999
        assert created_customer.name == "John Doe"
        assert created_customer.address == "123 Main St"
        assert created_customer.phone == "0789789789"
        
        # Check that creating a customer with an existing ID raises an error
        with pytest.raises(ValueError, match=r"Customer with ID 999 already exists"):
            self.manager.create(customer)  # Creating the same customer again should raise an error

    def test_read_customer(self):
        # Test reading an existing customer
        customer = self.manager.read(1)
        assert customer.customer_id == 1
        assert customer.name == "Existing Customer Name"  # Replace with actual data in customers.json
        assert customer.address == "Existing Address"  # Replace with actual data in customers.json
        assert customer.phone == "Existing Phone"  # Replace with actual data in customers.json

        # Test reading a non-existent customer raises KeyError
        with pytest.raises(KeyError):
            self.manager.read(9999)

    def test_update_customer(self):
        # Update the details of an existing customer
        updated_customer = Customer(customer_id=1, name="Updated Name", address="Updated Address", phone="Updated Phone")
        self.manager.update(updated_customer)

        # Read back the customer and verify updates
        customer = self.manager.read(1)
        assert customer.name == "Updated Name"
        assert customer.address == "Updated Address"
        assert customer.phone == "Updated Phone"

    def test_delete_customer(self):
        # Delete an existing customer
        self.manager.delete(1)

        # Verify the customer has been deleted
        with pytest.raises(KeyError):
            self.manager.read(1)

    def test_list_customers(self):
        # List all customers and verify the output
        customers = self.manager.list()
        # Update the following assertion according to the initial data in your customers.json
        assert len(customers) == 3  # Adjust based on the number of entries in your customers.json
