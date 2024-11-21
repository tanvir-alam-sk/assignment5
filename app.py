from flask import Flask;
from flask import jsonify;
from flask import request;
import os
import json

app=Flask(__name__);

@app.route("/",methods=["GET"])
def home():
    return "Welcome"


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


#  register route


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()


    # Validate input
    email=data.get('email')
    username = data.get('username')
    password = data.get('password')
    

    if not username or not email or not password:
        return jsonify({"error": "Username, Email and password are required"}), 400

    
    # Read existing users
    users = read_users()



    for user in users:
        if(user['username'] == username):
            return jsonify({"error": "Username already taken"}), 400
        elif(user['email'] == email):
            return jsonify({"error": "Email already taken"}), 400


    # Add the new user
    users.append({"username": username,"email":email, "password": password,"role":"user"})
    write_users(users)


    return jsonify({"message": "User registered successfully"}), 201


#  login route


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

    for user in users:
        if((user['email'] == email) and (user['password'] == password)):
            return jsonify({"message": "User logined successfully"}), 201
        else:
            return jsonify({"message": "Email or Password is not currect"}), 400


#   get login user

# GET /profile: View user-specific profile information
@app.route('/profile', methods=['GET'])
def profile():
    users = read_users()

    for user in users:
        if user['email'] == email:
            return jsonify({
                "name": user['name'],
                "email": user['email'],
                "password": user['password'],  # Hashed password
                "role": user['role']
            }), 200

    return jsonify({"error": "User not found"}), 404


if __name__== "__main__":
    app.run(debug=True,port=5001)