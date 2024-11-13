from argparse import ArgumentParser, Namespace
from cafe_project.product import ProductManager, Product
from cafe_project.customer import CustomerManager, Customer
import typer
from typing import Optional

app = typer.Typer()


product_manager = ProductManager()
customer_manager = CustomerManager()

@app.command()
def list_products():
    """Lists all products."""
    print(product_manager.list())

@app.command()
def create_product(name: str, price: float):
    """Creates a new product with a given name and price."""

    # Generate a new product_id, or let the ProductManager handle this
    new_product_id = len(product_manager.list()) + 1  # Example approach, if IDs are sequential

    # Create a Product instance
    product = Product(product_id=new_product_id, name=name, price=price)

    # Pass the Product instance to ProductManager
    product_manager.create(product)
    print(f"Product '{name}' created with price {price}")

# currently requires an id (int) but returns all products for some reason
@app.command()
def read_product(product_id:int):
    """Reads details of a specific product by ID."""
    product = product_manager.read(product_id)
    print(product)

@app.command()
def list_products():
    """Lists all products."""
    print(product_manager.list())

# #example use: python3 -m cafe_project.client_calls update 1 --name "Updated Name" --price 5.0
@app.command()
def update_product(product_id: int, name: Optional[str] = None, price: Optional[float] = None):
    """Updates an existing product's details by ID."""
    existing_product = product_manager.read(product_id)
    
    if not existing_product:
        print(f"Product with ID {product_id} not found.")
        return

    updated_product = Product(
        product_id=existing_product.product_id,
        name=name if name else existing_product.name,
        price=price if price is not None else existing_product.price
    )
    
    updated_model = product_manager.update(updated_product)
    print(f"Product {updated_model.product_id} updated: {updated_model}")


@app.command()
def delete_product(product_id: int):
    """Deletes a product by ID."""
    try:
        product_manager.delete(product_id)
        print(f"Product with ID {product_id} has been deleted.")
    except KeyError:
        print(f"Product with ID {product_id} not found.")



if __name__ == "__main__":
    app()
