from flask import Flask;
from flask import jsonify;
from flask import request;
import os
import json
from utility.jwt import create_jwt,verify_token
from flasgger import Swagger 
from db.token import jwt_token


app=Flask(__name__)
swagger = Swagger(app)

user_file_path = os.path.join("db", "users.py")


# Ensure the file exists
if not os.path.exists(user_file_path):
    with open("user_file_path", "w") as file:
        json.dump([], file)


# Function to read users from file
def read_users():
    """Simulates reading users from a data source"""
    with open(user_file_path, "r") as file:
        return json.load(file)


# Function to write users to file
def write_users(users):
    """Simulates writing users to a data source"""
    with open(user_file_path, "w") as file:
        json.dump(users, file, indent=4)



@app.route("/", methods=["GET"])
def home():
    """
    Home Page
    ---
    tags:
      - Welcome
    responses:
      200:
        description: Returns a welcome message
        examples:
          text/plain: "Welcome to User"
    """
    return "Welcome to User"



# POST /register: For Register a user with Username, Email And Password

@app.route('/register', methods=['POST'])
def register():
    """
    User Registration
    ---
    tags:
      - User Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: Desired username
              example: johndoe
            email:
              type: string
              description: User's email address
              example: johndoe@example.com
            password:
              type: string
              description: User's password
              example: "password123"
    responses:
      201:
        description: User registered successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User registered successfully"
      400:
        description: Input validation error or duplicate username/email
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Username, Email and password are required"
    """
    data = request.get_json()

    # Validate input
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({"error": "Username, Email and password are required"}), 400

    # Read existing users
    users = read_users()

    for user in users:
        if user['username'] == username:
            return jsonify({"error": "Username already taken"}), 400
        elif user['email'] == email:
            return jsonify({"error": "Email already taken"}), 400

    # Add the new user
    users.append({"username": username, "email": email, "password": password, "role": "user"})
    write_users(users)

    return jsonify({"message": "User registered successfully"}), 201



# POST /login: For Login a user with Email And Password
@app.route("/login", methods=["POST"])
def get_user():
    """
    User Login
    ---
    tags:
      - User Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: User's email address
              example: johndoe@example.com
            password:
              type: string
              description: User's password
              example: password123
    responses:
      201:
        description: Login successful
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User logined successfully"
      400:
        description: Login failed (e.g., missing credentials or incorrect login details)
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Email and password are required"
            message:
              type: string
              example: "Email or Password is not correct"
    """
    data = request.get_json()

    # Validate input
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Read existing users
    users = read_users()

    for user in users:
        if user['email'] == email and user['password'] == password:
            create_jwt(email)
            return jsonify({"message": "User logined successfully"}), 201

    return jsonify({"message": "Email or Password is not correct"}), 400


# GET /profile: View logined user-specific profile information

@app.route('/profile', methods=['GET'])
def  profile():
    """
    Get User Profile
    ---
    tags:
      - User Management
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: JWT token for user authentication
        example: "Bearer <your_token>"
    responses:
      200:
        description: User profile retrieved successfully
        schema:
          type: object
          properties:
            username:
              type: string
              example: johndoe
            email:
              type: string
              example: johndoe@example.com
            password:
              type: string
              example: password123
            role:
              type: string
              example: user
      404:
        description: User not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "User not found"
      401:
        description: Unauthorized access
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid or expired token"
    """
    # Simulate JWT verification
    jwt_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    logined_user_email = verify_token(jwt_token)

    if not logined_user_email:
        return jsonify({"error": "Invalid or expired token"}), 401

    # Read users
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


# Update /profile: View logined user-specific profile information
@app.route('/profile', methods=['PATCH'])
def  update_profile():
    """
    Update User Profile
    ---
    tags:
      - User Management
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: JWT token for user authentication
        example: "Bearer <your_token>"
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: The user's email (must match the logged-in user)
              example: johndoe@example.com
            username:
              type: string
              description: Updated username
              example: john_updated
            password:
              type: string
              description: Updated password
              example: newpassword123
            role:
              type: string
              description: Updated role
              example: admin
    responses:
      201:
        description: User information updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User Information Update successfully"
      403:
        description: Forbidden access (email mismatch)
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Forbidden Access"
      404:
        description: User not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "User not found"
      400:
        description: Bad request (missing or invalid data)
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Bad request"
    """
    jwt_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    logined_user_email = verify_token(jwt_token)

    if not logined_user_email:
        return jsonify({"error": "Invalid or expired token"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"error": "Bad request"}), 400

    if data.get('email') != logined_user_email:
        return jsonify({"error": "Forbidden Access"}), 403

    users = read_users()
    for user in users:
        if user['email'] == logined_user_email:
            for key, value in data.items():
                user[key] = value
            write_users(users)
            return jsonify({"message": "User Information Update successfully"}), 201

    return jsonify({"error": "User not found"}), 404



if __name__== "__main__":
    app.run(debug=True,port=5001)
