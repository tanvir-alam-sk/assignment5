from flask import request, jsonify
from model.user import register_user, authenticate_user, update_user_info, read_users, user_exists
from utility.jwt import create_jwt, verify_token


def home():
    return "Welcome to User"


def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Username, Email and password are required"}), 400

    if user_exists(username=username, email=email):
        return jsonify({"error": "Username or Email already taken"}), 400

    register_user(username, email, password)
    return jsonify({"message": "User registered successfully"}), 201


def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = authenticate_user(email, password)
    if user:
        create_jwt(email)
        return jsonify({"message": "User logged in successfully"}), 201

    return jsonify({"message": "Email or Password is not correct"}), 400


def get_profile():
    jwt_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    logined_user_email = verify_token(jwt_token)

    if not logined_user_email:
        return jsonify({"error": "Invalid or expired token"}), 401

    users = read_users()
    for user in users:
        if user['email'] == logined_user_email:
            return jsonify({
                "username": user['username'],
                "email": user['email'],
                "password": user['password'],
                "role": user['role']
            }), 200

    return jsonify({"error": "User not found"}), 404


def update_profile():
    jwt_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    logined_user_email = verify_token(jwt_token)

    if not logined_user_email:
        return jsonify({"error": "Invalid or expired token"}), 401

    data = request.get_json()
    if not data or data.get('email') != logined_user_email:
        return jsonify({"error": "Forbidden Access"}), 403

    updated_user = update_user_info(logined_user_email, data)
    if updated_user:
        return jsonify({"message": "User Information updated successfully"}), 201
    return jsonify({"error": "User not found"}), 404
