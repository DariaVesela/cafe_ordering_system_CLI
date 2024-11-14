from argparse import ArgumentParser, Namespace
from cafe_project.product import ProductManager, Product
from cafe_project.customer import CustomerManager, Customer
from cafe_project.order import OrderManager, Order
from cafe_project.courier import CourierManager, Courier
import typer
from typing import Optional
from datetime import datetime


app = typer.Typer()


product_manager = ProductManager()
customer_manager = CustomerManager()
order_manager = OrderManager()
courier_manager = CourierManager()

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

@app.command()
def list_orders():
    """Lists all orders."""
    orders = order_manager.list()
    for order in orders:
        print(order)

@app.command()
def create_order(
    date: int = typer.Option(..., help="The date of the order in YYYYMMDD format"),
    time: int = typer.Option(..., help="The time of the order in HHMM format (24-hour clock)"),
    courier_id: int = typer.Option(..., help="The ID of the courier handling the order"),
    products: str = typer.Option(..., help="Comma-separated list of product IDs in the order"),
    progress: int = typer.Option(..., help="The progress status of the order")
):
    """Creates a new order with the specified details, generating a unique order_id."""
    
    # Generate a new order ID based on the number of existing orders
    existing_orders = order_manager.list()
    new_order_id = max((order.order_id for order in existing_orders), default=0) + 1
    
    # Parse the products string into a list of integers
    product_ids = [int(pid.strip()) for pid in products.split(",")]
    product_list = [Product(product_id=pid, name=f"Product-{pid}", price=10.0) for pid in product_ids]
    
    # Create a new Order instance
    order = Order(
        date=date,
        time=time,
        order_id=new_order_id,
        courier_id=courier_id,
        products=product_list,
        progress=progress
    )
    
    try:
        order_manager.create(order)
        print(f"Order {new_order_id} created.")
    except ValueError as e:
        print(e)

@app.command()
def read_order(order_id: int):
    """Reads details of a specific order by ID."""
    try:
        order = order_manager.read(order_id)
        
        # Format date for display if it's stored as YYYYMMDD
        if isinstance(order.date, int):  # Check if date is stored as YYYYMMDD integer
            date_str = datetime.strptime(str(order.date), "%Y%m%d").strftime("%Y-%m-%d")
        else:
            date_str = order.date  # If date is already a string, use as-is

        # Print order details with formatted date
        print(f"Order ID: {order.order_id}")
        print(f"Date: {date_str}")
        print(f"Time: {order.time}")
        print(f"Courier ID: {order.courier_id}")
        print("Products:")
        for product in order.products:
            print(f"  - {product.name} (ID: {product.product_id}, Price: ${product.price})")
        print(f"Progress: {order.progress}")
        
    except KeyError:
        print(f"Order with ID {order_id} not found.")


@app.command()
def update_order(
    order_id: int,
    date: Optional[str] = None,
    time: Optional[int] = None,
    courier_id: Optional[int] = None,
    products: Optional[str] = None,
    progress: Optional[int] = None
):
    """Updates an existing order's details by ID."""
    try:
        # Retrieve the existing order
        existing_order = order_manager.read(order_id)
        
        # Parse the date if provided, otherwise keep existing date
        if date:
            try:
                parsed_date = int(datetime.strptime(date, "%Y-%m-%d").strftime("%Y%m%d"))
            except ValueError:
                print("Error: Date must be in YYYY-MM-DD format.")
                return
        else:
            parsed_date = existing_order.date

        # Fetch updated products from ProductManager if provided, otherwise keep existing products
        if products:
            product_ids = [int(pid.strip()) for pid in products.split(",")]
            product_list = []
            for pid in product_ids:
                try:
                    product = product_manager.read(pid)
                    product_list.append(product)
                except KeyError:
                    print(f"Warning: Product with ID {pid} not found in products2.json.")
        else:
            product_list = existing_order.products  # Keep existing products if no new products are provided
        
        # Create an updated Order instance with either the new or existing values
        updated_order = Order(
            date=parsed_date,
            time=time if time is not None else existing_order.time,
            order_id=existing_order.order_id,
            courier_id=courier_id if courier_id is not None else existing_order.courier_id,
            products=product_list,
            progress=progress if progress is not None else existing_order.progress
        )
        
        # Use OrderManager's existing update function to save the updated order
        order_manager.update(updated_order)
        print(f"Order {order_id} updated successfully.")
    
    except KeyError:
        print(f"Order with ID {order_id} not found.")


@app.command()
def delete_order(order_id: int):
    """Deletes an order by ID."""
    try:
        # Call OrderManager's delete method to remove the order
        order_manager.delete(order_id)
        print(f"Order with ID {order_id} has been deleted.")
    except KeyError:
        print(f"Order with ID {order_id} not found.")

@app.command()
def create_customer(
    name: str = typer.Option(..., help="The name of the customer"),
    address: str = typer.Option(..., help="The address of the customer"),
    phone: str = typer.Option(..., help="The phone number of the customer")
):
    """Creates a new customer with the specified details."""
    
    # Generate a unique customer_id based on the existing customers
    existing_customers = customer_manager.list()
    new_customer_id = max((customer.customer_id for customer in existing_customers), default=0) + 1
    
    # Create a Customer instance
    customer = Customer(customer_id=new_customer_id, name=name, address=address, phone=phone)
    
    # Use CustomerManager's create method to save the customer
    customer_manager.create(customer)
    print(f"Customer '{name}' created with ID {new_customer_id}")


@app.command()
def read_customer(customer_id: int):
    """Reads details of a specific customer by ID."""
    try:
        # Use CustomerManager's read method to retrieve the customer
        customer = customer_manager.read(customer_id)
        
        # Print customer details
        print(f"Customer ID: {customer.customer_id}")
        print(f"Name: {customer.name}")
        print(f"Address: {customer.address}")
        print(f"Phone: {customer.phone}")
        
    except KeyError:
        print(f"Customer with ID {customer_id} not found.")

@app.command()
def list_customers():
    """Lists all customers."""
    customers = customer_manager.list()  # Retrieve all customers
    
    if not customers:
        print("No customers found.")
    else:
        for customer in customers:
            print(f"Customer ID: {customer.customer_id}")
            print(f"Name: {customer.name}")
            print(f"Address: {customer.address}")
            print(f"Phone: {customer.phone}")
            print("-" * 20)  # Separator between customers

@app.command()
def update_customer(
    customer_id: int,
    name: Optional[str] = None,
    address: Optional[str] = None,
    phone: Optional[str] = None
):
    """Updates an existing customer's details by ID."""
    try:
        # Retrieve the existing customer
        existing_customer = customer_manager.read(customer_id)
        
        # Create an updated Customer instance with either the new or existing values
        updated_customer = Customer(
            customer_id=existing_customer.customer_id,
            name=name if name is not None else existing_customer.name,
            address=address if address is not None else existing_customer.address,
            phone=phone if phone is not None else existing_customer.phone
        )
        
        # Use CustomerManager's existing update method to save the updated customer
        customer_manager.update(updated_customer)
        print(f"Customer with ID {customer_id} updated successfully.")
    
    except KeyError:
        print(f"Customer with ID {customer_id} not found.")

@app.command()
def delete_customer(customer_id: int):
    """Deletes a customer by ID."""
    try:
        # Call CustomerManager's delete method to remove the customer
        customer_manager.delete(customer_id)
        print(f"Customer with ID {customer_id} has been deleted.")
    except KeyError:
        print(f"Customer with ID {customer_id} not found.")




if __name__ == "__main__":
    app()
