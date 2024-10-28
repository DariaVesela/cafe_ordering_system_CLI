from main.customer import CustomerManager
from main.entity_manager import JSONCRUDBase


def foo(repo: JSONCRUDBase):
    repo.delete(1)

if __name__ == '__main__':
    foo(CustomerManager()) 