from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from config import users_collection
import bcrypt

auth = Blueprint('auth', __name__)

# Регистрация
@auth.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    user = {
        "email": data["email"],
        "password": hashed_password.decode('utf-8')
    }
    users_collection.insert_one(user)
    return jsonify({"message": "User registered!"}), 201

# Логин
@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    user = users_collection.find_one({"email": data["email"]})
    if not user or not bcrypt.checkpw(data["password"].encode('utf-8'), user["password"].encode('utf-8')):
        return jsonify({"message": "Invalid credentials"}), 401
    access_token = create_access_token(identity=user["email"])
    return jsonify(access_token=access_token)

# Защищённый маршрут
@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
