from argparse import ArgumentParser, Namespace
from cafe_project.product import ProductManager, Product

product_manager = ProductManager()

def list_products():
    """Lists all products."""
    print(product_manager.list())

def create_product(args: Namespace):
    """Creates a new product with a given name and price."""

    # Generate a new product_id, or let the ProductManager handle this
    new_product_id = len(product_manager.list()) + 1  # Example approach, if IDs are sequential

    # Create a Product instance
    product = Product(product_id=new_product_id, name=args.name, price=args.price)

    # Pass the Product instance to ProductManager
    product_manager.create(product)
    print(f"Product '{args.name}' created with price {args.price}")

# currently requires an id (int) but returns all products for some reason
def read_product(args: Namespace):
    """Reads details of a specific product by ID."""
    product = product_manager.read(args.product_id)
    print(product)

#example use: python3 -m cafe_project.client_calls update 1 --name "Updated Name" --price 5.0
def update_product(args):
    """Updates an existing product's details by ID."""
    # Retrieve the existing product
    existing_product = product_manager.read(args.product_id)
    
    if not existing_product:
        print(f"Product with ID {args.product_id} not found.")
        return

    # Create a new Product instance, using existing values if new ones aren't provided
    updated_product = Product(
        product_id=existing_product.product_id,
        name=args.name if args.name else existing_product.name,
        price=args.price if args.price is not None else existing_product.price
    )
    
    # Pass the updated Product instance to the update method
    updated_model = product_manager.update(updated_product)
    print(f"Product {updated_model.product_id} updated: {updated_model}")

#works just fineeee!!!
def delete_product(args: Namespace):
    """Deletes a product by ID."""
    product_manager.delete(args.product_id)
    print(f"Product {args.product_id} deleted")

def main():
    parser = ArgumentParser(description="Manage products in the cafe")
    subparsers = parser.add_subparsers(title="commands", dest="command", required=True)

    # List products
    subparsers.add_parser("list", help="List all products")

    # Create product
    create_parser = subparsers.add_parser("create", help="Create a new product")
    create_parser.add_argument("name", type=str, help="Name of the product")
    create_parser.add_argument("price", type=float, help="Price of the product")

    # Read product
    read_parser = subparsers.add_parser("read", help="Read product details by ID")
    read_parser.add_argument("product_id", type=int, help="ID of the product")

    # Update product
    update_parser = subparsers.add_parser("update", help="Update a product by ID")
    update_parser.add_argument("product_id", type=int, help="ID of the product")
    update_parser.add_argument("--name", type=str, required=False, help="New name of the product")
    update_parser.add_argument("--price", type=float, required=False, help="New price of the product")

    # Delete product
    delete_parser = subparsers.add_parser("delete", help="Delete a product by ID")
    delete_parser.add_argument("product_id", type=int, help="ID of the product to delete")

    # Parse arguments
    args = parser.parse_args()

    # Dispatch commands to the appropriate function
    if args.command == "list":
        list_products()
    elif args.command == "create":
        create_product(args)
    elif args.command == "read":
        read_product(args)
    elif args.command == "update":
        update_product(args)
    elif args.command == "delete":
        delete_product(args)

if __name__ == "__main__":
    main()
