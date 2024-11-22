from flask import Flask;
from flask import jsonify;
from flask import request;
import os
import json
from utility.jwt import create_jwt,verify_token

from db.token import jwt_token


app=Flask(__name__)


user_file_path = os.path.join("db", "users.py")


# Ensure the file exists
if not os.path.exists(user_file_path):
    with open("user_file_path", "w") as file:
        json.dump([], file)


# Function to read users from file
def read_users():
    with open(user_file_path, "r") as file:
        return json.load(file)


# Function to write users to file
def write_users(users):
    with open(user_file_path, "w") as file:
        json.dump(users, file, indent=4)


# Ensure user exists
# def find_ligin_user(users,email,password):
#     for user in users:
#         if((user['email'] == email) and (user['password'] == password)):
#             find_user=1
#             create_jwt(email)
#             return jsonify({"message": "User logined successfully"}), 201

#     if(find_user==-1):
#         return jsonify({"message": "Email or Password is not currect"}), 400



@app.route("/",methods=["GET"])
def home():
    return "Welcome"



# POST /register: For Register a user with Username, Email And Password

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()


    # Validate input
    username = data.get('username')
    email=data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({"error": "Username, Email and password are required"}), 400

    # Read existing users
    users = read_users()
    # find_ligin_user(user,)

    for user in users:
        if(user['username'] == username):
            return jsonify({"error": "Username already taken"}), 400
        elif(user['email'] == email):
            return jsonify({"error": "Email already taken"}), 400

    # Add the new user
    users.append({"username": username,"email":email, "password": password,"role":"user"})
    write_users(users)

    return jsonify({"message": "User registered successfully"}), 201



# POST /login: For Login a user with Email And Password
@app.route("/login",methods=["POST"])
def get_user():
    data = request.get_json()

    # Validate input
    email=data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Read existing users
    users = read_users();

    find_user=-1
    for user in users:
        if((user['email'] == email) and (user['password'] == password)):
            find_user=1
            create_jwt(email)
            return jsonify({"message": "User logined successfully"}), 201

    if(find_user==-1):
        return jsonify({"message": "Email or Password is not currect"}), 400


# GET /profile: View logined user-specific profile information

@app.route('/profile', methods=['GET'])
def update_profile():
    logined_user_email=verify_token(jwt_token)
    users = read_users()

    for user in users:
        if user['email'] ==  logined_user_email:
            return jsonify({
                "username": user['username'],
                "email": user['email'],
                "password": user['password'], 
                "role": user['role']
            }), 200

    return jsonify({"error": "User not found"}), 404


# Update /profile: View logined user-specific profile information
@app.route('/profile', methods=['PATCH'])
def profile():
    logined_user_email=verify_token(jwt_token)
    users = read_users()
    find_user=-1;

    data = request.get_json();


    if(data['email'] != logined_user_email):
        return jsonify({"error": "Forbidden Access"}), 403


    for user in users:
        if((user['email'] == logined_user_email)):
            find_user=1
            for key, value in data.items():
                user[key]=value;
                write_users(users)
            return jsonify({"message": "User Information Update successfully"}), 201
    
    if(find_user==-1):
        return jsonify({"error": "User not found"}), 404



if __name__== "__main__":
    app.run(debug=True,port=5001)
