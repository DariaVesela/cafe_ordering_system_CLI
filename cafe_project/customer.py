
import json
from dataclasses import dataclass
from pathlib import Path
from cafe_project.entity_manager import JSONCRUDBase

@dataclass
class Customer(BaseModel):
    customer_id: int
    name: str
    address: str
    phone: str


class CustomerManager(JSONCRUDBase):
    def __init__(self):
        json_file = Path('src/main/data/customers.json')
        super().__init__(json_file)

    def create(self, customer: Customer) -> Customer:
        customers = self._read_from_json()
        customers[customer.customer_id] = customer.__dict__
        self._write_to_json(customers)
        return customer

    def read(self, customer_id: int) -> Customer:
        customers = self._read_from_json()
        return Customer(**customers[customer_id])
    
    def list(self)-> list[Customer]:
        data=self._read_from_json()
        list_of_customers: list[Customer] =[]
        for entity in data.values():
            list_of_customers.append(Customer(**entity))
        
        return list_of_customers
    
    def update(self, customer: Customer) -> Customer:
            data = self._read_from_json()
            # Delete the old customer if it exists
            if str(customer.customer_id) in data:
                del data[str(customer.customer_id)]
            # Add the new customer
            data[str(customer.customer_id)] = customer.__dict__
            self._write_to_json(data=data)
            return customer
    
    def delete(self, customer_id: int) -> None:
        data=self._read_from_json()
        del data[str(customer_id)]
        self._write_to_json(data=data)

#example model = Customer(customer_id=1, name='John Doe', address='123 Main St', phone='0789789789')

# manager = CustomerManager()
# manager.update(Customer(customer_id=1, name='John Doe', address='123 Main St', phone='0789789789'))

# print(manager.list())
