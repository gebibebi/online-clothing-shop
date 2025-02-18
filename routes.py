from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from auth import auth
from config import products_collection, users_collection, orders_collection

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = "your_secret_key"
jwt = JWTManager(app)
app.register_blueprint(auth, url_prefix="/api/auth")

# ✅ Получить всех пользователей
@app.route('/api/users', methods=['GET'])
def get_users():
    users = list(users_collection.find({}, {"_id": 0}))
    return jsonify(users)

# ✅ Получить все заказы
@app.route('/api/orders', methods=['GET'])
def get_orders():
    orders = list(orders_collection.find({}, {"_id": 0}))
    return jsonify(orders)

# ✅ Получить все товары
@app.route('/api/products', methods=['GET'])
def get_products():
    products = list(products_collection.find({}, {"_id": 0}))
    return jsonify(products)

# ✅ Добавить товар
@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    products_collection.insert_one(data)
    return jsonify({"message": "Товар добавлен"}), 201

# ✅ Обновить товар
@app.route('/api/products/<string:product_name>', methods=['PUT'])
def update_product(product_name):
    data = request.json
    products_collection.update_one({"product_name": product_name}, {"$set": data})
    return jsonify({"message": "Товар обновлён"})

# ✅ Удалить товар
@app.route('/api/products/<string:product_name>', methods=['DELETE'])
def delete_product(product_name):
    products_collection.delete_one({"product_name": product_name})
    return jsonify({"message": "Товар удалён"})

# ✅ Маршрут для проверки работы API
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Online Clothing Shop API!"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
