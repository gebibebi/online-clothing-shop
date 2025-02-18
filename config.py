from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "online_clothing_shop"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

products_collection = db["products"]
users_collection = db["users"]
orders_collection = db["orders"]

# Оптимизация базы (индексы)
products_collection.create_index([("product_name", "text")])
orders_collection.create_index([("order_id", 1)])
users_collection.create_index([("email", 1)], unique=True)  # Закрыли скобку!
