import abc
import json
from pathlib import Path
from typing import Any


class JSONCRUDBase(abc.ABC):

    def __init__(self, json_file: Path):
        self.json_file = json_file

    def _read_from_json(self) -> dict[str,Any]:
        try:
            with open(self.json_file.absolute(), 'r') as file:
                return json.load(file)
        except (FileNotFoundError,json.decoder.JSONDecodeError):
            return {}
        
    def _write_to_json(self, data: dict[str,Any]) -> None:
        with open(self.json_file.absolute(), 'w') as file:
            json.dump(data, file, indent=4)


    @abc.abstractmethod
    def create(self, model: Any) -> Any:
        ...
    @abc.abstractmethod
    def read(self, id: Any) -> Any:
         ...
    @abc.abstractmethod
    def update(self, model: Any) -> Any:
         ...
    @abc.abstractmethod
    def delete(self, id: Any) -> None:
        ...
    @abc.abstractmethod
    def list(self)-> list[Any]:
        ...