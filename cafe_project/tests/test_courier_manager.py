import pytest
from cafe_project.courier import CourierManager, Courier
from pathlib import Path
import json
import shutil

class TestCourierManager:
    def setup_method(self):
        # Define paths
        self.original_file = Path("cafe_project/data/couriers.json")
        self.test_file = Path("cafe_project/data/test_couriers.json")
        
        # Copy the original couriers.json to test_couriers.json
        shutil.copy(self.original_file, self.test_file)
        
        # Create a CourierManager instance with the test file
        self.manager = CourierManager()
        self.manager._json_file = self.test_file  # Use the test file for all operations

    def teardown_method(self):
        # Delete the test file after each test to clean up
        if self.test_file.exists():
            self.test_file.unlink()

    def test_create_courier(self):
        # Test creating a new courier
        courier = Courier(courier_id=999, name="John Smith", phone="0789789789")
        self.manager.create(courier)
        
        # Read back the courier to verify
        created_courier = self.manager.read(999)
        assert created_courier.courier_id == 999
        assert created_courier.name == "John Smith"
        assert created_courier.phone == "0789789789"
        
        # Check that creating a courier with an existing ID raises an error
        with pytest.raises(ValueError, match=r"Courier with ID 999 already exists"):
            self.manager.create(courier)  # Creating the same courier again should raise an error

    def test_read_courier(self):
        # Test reading an existing courier
        courier = self.manager.read(1)
        assert courier.courier_id == 1
        assert courier.name == "Existing Courier Name"  # Replace with actual data in couriers.json
        assert courier.phone == "Existing Phone"  # Replace with actual data in couriers.json

        # Test reading a non-existent courier raises KeyError
        with pytest.raises(KeyError):
            self.manager.read(9999)

    def test_update_courier(self):
        # Update the details of an existing courier
        updated_courier = Courier(courier_id=1, name="Updated Courier Name", phone="Updated Phone")
        self.manager.update(updated_courier)

        # Read back the courier and verify updates
        courier = self.manager.read(1)
        assert courier.name == "Updated Courier Name"
        assert courier.phone == "Updated Phone"

    def test_delete_courier(self):
        # Delete an existing courier
        self.manager.delete(1)

        # Verify the courier has been deleted
        with pytest.raises(KeyError):
            self.manager.read(1)

    def test_list_couriers(self):
        # List all couriers and verify the output
        couriers = self.manager.list()
        # Update the following assertion according to the initial data in your couriers.json
        assert len(couriers) == 3  # Adjust based on the number of entries in your couriers.json
