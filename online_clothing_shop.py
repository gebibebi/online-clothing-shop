import json
import requests
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['online_clothing_shop']
products_collection = db['products']
scraped_products_collection = db['scraped_products']  # Collection for scraped data
users_collection = db['users']
orders_collection = db['orders']

# Function to load JSON data and insert it into the database
def load_data_from_json(file_path, collection):
    """Load data from a JSON file into the specified MongoDB collection."""
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)  # Load data from JSON file
            result = collection.insert_many(data)  # Insert into MongoDB
            print(f"{len(result.inserted_ids)} records added successfully!")
    except Exception as e:
        print(f"Error loading JSON data: {e}")

# Function to create (insert) a new record
def create_record(record, collection):
    """Add a new record to the specified MongoDB collection."""
    try:
        if not collection.find_one({"id": record["id"]}):
            result = collection.insert_one(record)
            print(f"Record added successfully with ID: {result.inserted_id}")
        else:
            print(f"Record with ID {record['id']} already exists.")
    except Exception as e:
        print(f"Error creating record: {e}")

# Function to get all records
def get_all_records(collection):
    """Retrieve and display all records from the specified MongoDB collection."""
    try:
        records = list(collection.find())
        if records:
            print("Available records:")
            for record in records:
                print(record)
        else:
            print("No records found.")
    except Exception as e:
        print(f"Error retrieving records: {e}")

# Function to update a record by ID
def update_record_by_id(record_id, update_fields, collection):
    """Update an existing record by its ID in the specified MongoDB collection."""
    try:
        result = collection.update_one({"id": record_id}, {"$set": update_fields})
        if result.matched_count > 0:
            print(f"Record with ID {record_id} updated successfully!")
        else:
            print(f"Record with ID {record_id} not found.")
    except Exception as e:
        print(f"Error updating record: {e}")

# Function to delete a record by name
def delete_record_by_name(record_name, collection):
    """Delete a record by its name from the specified MongoDB collection."""
    try:
        result = collection.delete_one({"product_name": record_name})
        if result.deleted_count > 0:
            print(f"Record '{record_name}' deleted successfully.")
        else:
            print(f"Record '{record_name}' not found.")
    except Exception as e:
        print(f"Error deleting record: {e}")

# Function to delete a record by ID
def delete_record_by_id(record_id, collection):
    """Delete a record by its ID from the specified MongoDB collection."""
    try:
        result = collection.delete_one({"id": record_id})
        if result.deleted_count > 0:
            print(f"Record with ID {record_id} deleted successfully.")
        else:
            print(f"Record with ID {record_id} not found.")
    except Exception as e:
        print(f"Error deleting record: {e}")

# Function for local file scraping
def scrape_local_file(file_path):
    """Scrape product data from a local HTML file."""
    scraped_data = []
    try:
        with open(file_path, 'r') as file:
            soup = BeautifulSoup(file, 'html.parser')
            products = soup.find_all('div', class_='product-card')  # Replace with real selectors
            for product in products:
                try:
                    name = product.find('h2', class_='product-name').text.strip()
                    price = product.find('span', class_='product-price').text.strip()
                    category = product.find('span', class_='product-category').text.strip()
                    scraped_data.append({
                        "name": name,
                        "price": price,
                        "category": category
                    })
                except AttributeError:
                    continue
        print(f"{len(scraped_data)} products scraped from the local file.")
    except Exception as e:
        print(f"Error reading the file: {e}")
    return scraped_data

# Save scraped data to MongoDB
def save_to_mongo(data, collection):
    """Save scraped data to MongoDB."""
    try:
        if data:
            collection.insert_many(data)
            print(f"{len(data)} records inserted successfully!")
        else:
            print("No data to save.")
    except Exception as e:
        print(f"Error saving to MongoDB: {e}")

# Main interaction loop
if __name__ == "__main__":
    try:
        products_path = '/Users/dilnazshanova/Desktop/OnlineClothingShop/products.json'
        users_path = '/Users/dilnazshanova/Desktop/OnlineClothingShop/users.json'
        orders_path = '/Users/dilnazshanova/Desktop/OnlineClothingShop/orders.json'

        load_data_from_json(products_path, products_collection)
        load_data_from_json(users_path, users_collection)
        load_data_from_json(orders_path, orders_collection)
        print("All JSON data imported successfully!")
    except Exception as e:
        print(f"Error importing JSON data: {e}")

    while True:
        print("\nOptions:")
        print("1. Load products from JSON file")
        print("2. Load users from JSON file")
        print("3. Load orders from JSON file")
        print("4. Create a new product")
        print("5. Create a new user")
        print("6. Create a new order")
        print("7. Get all products")
        print("8. Get all users")
        print("9. Get all orders")
        print("10. Update a product by ID")
        print("11. Update a user by ID")
        print("12. Update an order by ID")
        print("13. Delete a product by name")
        print("14. Delete a user by name")
        print("15. Delete an order by ID")
        print("16. Scrape local file for products")
        print("17. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            file_path = input("Enter the path to the JSON file for products: ")
            load_data_from_json(file_path, products_collection)
        elif choice == "2":
            file_path = input("Enter the path to the JSON file for users: ")
            load_data_from_json(file_path, users_collection)
        elif choice == "3":
            file_path = input("Enter the path to the JSON file for orders: ")
            load_data_from_json(file_path, orders_collection)
        elif choice == "4":
            product = {
                "id": int(input("Enter product ID: ")),
                "product_name": input("Enter product name: "),
                "product_category": input("Enter product category: "),
                "size": input("Enter size: "),
                "price": float(input("Enter price: ")),
                "stock": int(input("Enter stock: ")),
                "brand": input("Enter brand: "),
                "color": input("Enter color: "),
                "material": input("Enter material: "),
                "release_date": input("Enter release date (MM/DD/YYYY): ")
            }
            create_record(product, products_collection)
        elif choice == "5":
            user = {
                "id": int(input("Enter user ID: ")),
                "first_name": input("Enter first name: "),
                "last_name": input("Enter last name: "),
                "email": input("Enter email: "),
                "gender": input("Enter gender: "),
                "phone": input("Enter phone: "),
                "address": {
                    "street": input("Enter street address: "),
                    "city": input("Enter city: "),
                    "state": input("Enter state: "),
                    "zip": input("Enter ZIP code: ")
                },
                "registration_date": input("Enter registration date (MM/DD/YYYY): ")
            }
            create_record(user, users_collection)
        elif choice == "6":
            order = {
                "id": int(input("Enter order ID: ")),
                "user_id": int(input("Enter user ID: ")),
                "order_date": input("Enter order date (MM/DD/YYYY): "),
                "status": input("Enter status: "),
                "total_price": float(input("Enter total price: ")),
                "products": [
                    {
                        "product_id": int(input("Enter product ID: ")),
                        "quantity": int(input("Enter quantity: ")),
                        "price": float(input("Enter price: "))
                    }
                ],
                "shipping_address": input("Enter shipping address: "),
                "payment_method": input("Enter payment method: ")
            }
            create_record(order, orders_collection)
        elif choice == "7":
            get_all_records(products_collection)
        elif choice == "8":
            get_all_records(users_collection)
        elif choice == "9":
            get_all_records(orders_collection)
        elif choice == "10":
            record_id = int(input("Enter product ID to update: "))
            update_fields = {}
            while True:
                field = input("Enter the field to update (type 'done' to finish): ")
                if field == "done":
                    break
                value = input(f"Enter the new value for {field}: ")
                update_fields[field] = value
            update_record_by_id(record_id, update_fields, products_collection)
        elif choice == "11":
            record_id = int(input("Enter user ID to update: "))
            update_fields = {}
            while True:
                field = input("Enter the field to update (type 'done' to finish): ")
                if field == "done":
                    break
                value = input(f"Enter the new value for {field}: ")
                update_fields[field] = value
            update_record_by_id(record_id, update_fields, users_collection)
        elif choice == "12":
            record_id = int(input("Enter order ID to update: "))
            update_fields = {}
            while True:
                field = input("Enter the field to update (type 'done' to finish): ")
                if field == "done":
                    break
                value = input(f"Enter the new value for {field}: ")
                update_fields[field] = value
            update_record_by_id(record_id, update_fields, orders_collection)
        elif choice == "13":
            record_name = input("Enter the product name to delete: ")
            delete_record_by_name(record_name, products_collection)
        elif choice == "14":
            record_name = input("Enter the user name to delete: ")
            delete_record_by_name(record_name, users_collection)
        elif choice == "15":
            record_id = int(input("Enter the order ID to delete: "))
            delete_record_by_id(record_id, orders_collection)
        elif choice == "16":
            print("Starting local file scraping...")
            file_path = input("Enter the path to the local HTML file: ")
            scraped_data = scrape_local_file(file_path)
            save_to_mongo(scraped_data, scraped_products_collection)
        elif choice == "17":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
