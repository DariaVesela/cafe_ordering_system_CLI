from dataclasses import dataclass
import json
from pathlib import Path
from pydantic import BaseModel, Field
from cafe_project.entity_manager import JSONCRUDBase


class Courier(BaseModel):
       
        courier_id: int
        name: str
        phone: str

class CourierManager(JSONCRUDBase):
        
        def __init__(self):
            json_file = Path(__file__).parent/'data'/'couriers.json'
            super().__init__(json_file)

        def create(self, courier: Courier) -> Courier:
            couriers = self._read_from_json()
            couriers[courier.courier_id] = courier.__dict__
            self._write_to_json(couriers)
            return courier
        
        #reads a concrete courier, wants the id as a STRING!
        def read(self, courier_id: int) -> Courier:
            couriers = self._read_from_json()
            return Courier(**couriers[courier_id])
        
        # returns a list of all couriers
        def list(self)-> list[Courier]:
            data=self._read_from_json()
            list_of_couriers: list[Courier] =[]
            for entity in data.values():
                list_of_couriers.append(Courier(**entity))
            
            return list_of_couriers
        
        # updates a courier
        # currently reshuffles the order of the couriers in the json file but I think that's fine(?)

        def update(self, courier: Courier) -> Courier:
                data = self._read_from_json()
                # Delete the old courier if it exists
                if str(courier.courier_id) in data:
                    del data[str(courier.courier_id)]
                # Add the new courier
                data[str(courier.courier_id)] = courier.__dict__
                self._write_to_json(data=data)
                return courier
        
        # deletes a courier, takes an integer as an argument
        def delete(self, courier_id: int) -> None:
            data=self._read_from_json()
            del data[str(courier_id)]
            self._write_to_json(data=data)
            

#manager = CourierManager()
#print(manager.read('3'))

#print(manager.list())