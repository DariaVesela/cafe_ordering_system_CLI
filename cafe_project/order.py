from dataclasses import dataclass
from typing import List
import json
from pathlib import Path
from pydantic import BaseModel, Field
from cafe_project.product import Product
from cafe_project.entity_manager import JSONCRUDBase


class Order(BaseModel):
    date: int
    time: int
    order_id: int
    courier_id: int
    products: List[Product]
    progress: int


class OrderManager(JSONCRUDBase):
    def __init__(self):
        json_file = Path(__file__).parent/'data'/'orders.json'
        super().__init__(json_file)

#add validation for duplicates 
# check the data structure of order - why is it a string?
#Current writing into file kinda ugly and unreadable
    def create (self, order: Order) -> Order:
        orders = self._read_from_json()
        # Check for duplicate order ID
        if str(order.order_id) in orders:
            raise ValueError(f"Order with ID {order.order_id} already exists.")
        orders[str(order.order_id)] = order.model_dump()
        self._write_to_json(orders)
        return order
    
    #reads a concrete order, currently expects order_id to be a string (because it is created as a string in the json file!!!)
    def read(self, order_id: int) -> Order:
        orders = self._read_from_json()
        return Order.model_validate_json(orders[order_id])
    
    # returns a list of all orders
    #works fine, output ugly though
    def list(self)-> list[Order]:
        data=self._read_from_json()
        list_of_orders: list[Order] =[]
        for entity in data.values():
            list_of_orders.append(Order.model_validate((entity)))
        
        return list_of_orders
    
    # updates an order
    # currently expects THE WHOLE ORDER, should probably only want an order_id and than ask what does the user want to update -> but this should probably be handled in the client_calls.py

    def update(self, order: Order) -> Order:
            data = self._read_from_json()
            # Delete the old order if it exists
            if str(order.order_id) in data:
                del data[str(order.order_id)]
            # Add the new order
            data[str(order.order_id)] = order.model_dump()
            self._write_to_json(data=data)
            return order
    
    # deletes an order
    def delete(self, order_id: int) -> None:
        data=self._read_from_json()
        del data[str(order_id)]
        self._write_to_json(data=data)

    # example product     
    # "2": {
    #     "product_id": 2,
    #     "name": "Cake",
    #     "price": 9.0
    # },

# #CREATE
manager = OrderManager()
manager.create(order=Order(date=132022, time=1150, order_id=4, courier_id=2, products=[Product(product_id=2, name='Cake', price=9)], progress=1))
print(manager.list())


# #READ
# manager = OrderManager()
# print(manager.read(order_id=2))
#print(manager.list())


#UPDATE

# manager = OrderManager()
# order = Order(
#     date='122024',
#     time='1050',
#     order_id='2',
#     courier_id=1,
#     products=[
#         Product(
#             product_id=2,
#             name="Cake",
#             price=9.0
#         )
#     ],
#     progress='1'
# )

# manager.update(order)
# print(manager.list())

#DELETE
# order=Order(
#     date=122024,
#     time=1050,
#     order_id=2,
#     courier_id=1,
#     products=[
#         Product(
#             product_id=2,
#             name="Cake",
#             price=9.0
#         )
#     ],
#     progress=1
# )

# manager = OrderManager()
# manager.delete(
#     order_id=2
# )
# print(manager.list())

