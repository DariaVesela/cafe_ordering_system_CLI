from dataclasses import dataclass
from typing import List
import json
from pathlib import Path
from pydantic import BaseModel, Field
from cafe_project.product import product
from cafe_project.entity_manager import JSONCRUDBase

@dataclass
class Order(BaseModel):
    date: int
    time: int
    order_id: int
    products: List[product]
    progress: int

class OrderManager(JSONCRUDBase):
    def __init__(self):
        json_file = Path('src/main/data/orders.json')
        super().__init__(json_file)

    def create (self, order: Order) -> Order:
        orders = self._read_from_json()
        orders[order.order_id] = order.__dict__
        self._write_to_json(orders)
        return order
    
    #reads a concrete order
    def read(self, order_id: int) -> Order:
        orders = self._read_from_json()
        return Order(**orders[order_id])
    
    # returns a list of all orders
    def list(self)-> list[Order]:
        data=self._read_from_json()
        list_of_orders: list[Order] =[]
        for entity in data.values():
            list_of_orders.append(Order(**entity))
        
        return list_of_orders
    
    # updates an order
    def update(self, order: Order) -> Order:
            data = self._read_from_json()
            # Delete the old order if it exists
            if str(order.order_id) in data:
                del data[str(order.order_id)]
            # Add the new order
            data[str(order.order_id)] = order.__dict__
            self._write_to_json(data=data)
            return order
    
    # deletes an order
    def delete(self, order_id: int) -> None:
        data=self._read_from_json()
        del data[str(order_id)]
        self._write_to_json(data=data)

    