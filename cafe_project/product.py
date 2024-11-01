from dataclasses import dataclass
import json
from pathlib import Path
from pydantic import BaseModel, Field
from cafe_project.entity_manager import JSONCRUDBase



class Product(BaseModel):
    product_id: int
    name: str
    price: float = Field(ge=0)
    
class ProductManager(JSONCRUDBase):
    def __init__(self):
        # This file location
        json_file = Path(__file__).parent/'data'/'products2.json'

        super().__init__(json_file)

    def create(self, model: Product) -> Product:
        data=self._read_from_json()
        data[model.product_id] = model.model_dump()
        self._write_to_json(data=data)
        return model
    
#list all products
    def list(self)-> list[Product]:
        data=self._read_from_json()
        list_of_products: list[Product] =[]
        for entity in data.values():
            list_of_products.append(Product(**entity))
        
        return list_of_products
    
    # exact implementation of this might need changes when handling user requests - should only require product name (UI wise should also offer a dropdown list) and the only thing that should be updated is the price
    def update(self, model: Product) -> Product:
            data = self._read_from_json()
            # Delete the old product if it exists
            if str(model.product_id) in data:
                del data[str(model.product_id)]
            # Add the new product
            data[str(model.product_id)] = model.model_dump()
            self._write_to_json(data=data)
            return model

    def delete(self, product_id: int) -> None:
        data=self._read_from_json()
        del data[str(product_id)]
        self._write_to_json(data=data)

#read a concrete product
    def read(self, product_id: int) -> Product:
        data=self._read_from_json()
        return Product(**data[str(product_id)])
        


#example model = Product(product_id=1, name='Chocolate', price=5)
manager = ProductManager()
manager.create(Product(product_id=2, name='Cake', price=9))

print(manager.list())

# manager = ProductManager()
# manager.delete(1)

# print(manager.list())