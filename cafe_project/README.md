# dasha-mini-project

# Cafe Project

**Version**: 0.1.0  
**Author**: Daria V ([vesela.dasha123@gmail.com](mailto:vesela.dasha123@gmail.com))  

## Description

This project, **Cafe Project**, is built using Python 3.13 and is structured as a modern Python project managed with [Poetry](https://python-poetry.org/). It includes utilities and dependencies to support type checking, data validation, command-line interface (CLI) creation, and testing.

## Features

- **Type Checking**: Built-in support for static type checking using `mypy`.
- **Data Validation**: Utilizes `pydantic` for robust data validation and parsing.
- **CLI Development**: Powered by `typer` for creating intuitive and powerful command-line interfaces.
- **Testing**: Comprehensive testing support with `pytest`.

## Installation

### Prerequisites

- Python 3.13 or higher.
- [Poetry](https://python-poetry.org/docs/#installation) installed on your system.

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd cafe_project


## HOW TO USE THE CLI: 

- To interact with the app, run the client_calls file from your terminal. 
- The available commands have been created using Typer and follow the format **action-object**,
- e.g. delete-order, list-products etc.
- If you're stuck, type **--help** to see all available commands:

## CLI MANUAL: 

## Command Reference

### Product Commands

- **list-products**  
  Lists all products.

- **create-product**  
  Creates a new product with a given name and price.  
  Flags: `--product_id`, `--name`, `--price`  
  Example usage:  
  ```bash
  create-product milkshake 6
  ```

- **read-product**  
  Reads details of a specific product by ID.  
  Example usage:  
  ```bash
  read-product 1
  ```

- **update-product**  
  Updates an existing product's details by ID.  
  Example usage:  
  ```bash
  update-product 1 --name "New Name"
  ```

- **delete-product**  
  Deletes a product by ID.  
  Example usage:  
  ```bash
  delete-product 6
  ```

---

### Order Commands

- **list-orders**  
  Lists all orders.  
  Example usage:  
  ```bash
  list-orders
  ```

- **create-order**  
  Creates a new order with the specified details, generating a unique `order_id`.  
  Flags: `--date yyyymmdd`, `--time hhmm`, `--courier-id iii`, `--products "int,int,int"`, `--progress int`  
  Example usage:  
  ```bash
  create-order --date 20231113 --time 1430 --courier-id 101 --products "1,2,3" --progress 0
  ```

- **read-order**  
  Reads details of a specific order by ID.  
  Example usage:  
  ```bash
  read-order 1
  ```

- **update-order**  
  Updates an existing order's details by ID.  
  Example usage:  
  ```bash
  update-order 1 --date 2023-11-15 --time 1500 --courier-id 102 --products "1,2" --progress 1
  ```

- **delete-order**  
  Deletes an order by ID.  
  Example usage:  
  ```bash
  delete-order 4
  ```

---

### Customer Commands

- **create-customer**  
  Creates a new customer with the specified details.  
  Flags: `--name "str"`, `--address "str"`, `--phone "str"`  
  Example usage:  
  ```bash
  create-customer --name "Keith Starmer" --address "10 Downing Street" --phone "0789678567"
  ```

- **read-customer**  
  Reads details of a specific customer by ID.  
  Example usage:  
  ```bash
  read-customer 3
  ```

- **list-customers**  
  Lists all customers.  
  Example usage:  
  ```bash
  list-customers
  ```

- **update-customer**  
  Updates an existing customer's details by ID.  
  Example usage:  
  ```bash
  update-customer 2 --name "Keeanu Reeves" --address "123 Cool Drive" --phone "07896789567"
  ```

- **delete-customer**  
  Deletes a customer by ID.  
  Example usage:  
  ```bash
  delete-customer 1
  ```

---

### Courier Commands

- **create-courier**  
  Creates a new courier with the specified details.  
  Flags: `--name`, `--phone`  
  Example usage:  
  ```bash
  create-courier --name "Michael Jackson" --phone "071233456256"
  ```

- **read-courier**  
  Reads details of a specific courier by ID.  
  Example usage:  
  ```bash
  read-courier 2
  ```

- **list-couriers**  
  Lists all couriers.  
  Example usage:  
  ```bash
  list-couriers
  ```

- **update-courier**  
  Updates an existing courier's details by ID.  
  Example usage:  
  ```bash
  update-courier 2 --name "Joanne of Arc" --phone "07987654321"
  ```

- **delete-courier**  
  Deletes a courier by ID.  
  Example usage:  
  ```bash
  delete-courier 1
  ```


