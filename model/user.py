import os
import json
from utility.jwt import create_jwt, verify_token

user_file_path = os.path.join("db", "users.py")

# Ensure the file exists
if not os.path.exists(user_file_path):
    with open(user_file_path, "w") as file:
        json.dump([], file)


def read_users():
    """Simulates reading users from a data source"""
    with open(user_file_path, "r") as file:
        return json.load(file)


def write_users(users):
    """Simulates writing users to a data source"""
    with open(user_file_path, "w") as file:
        json.dump(users, file, indent=4)


def user_exists(username=None, email=None):
    """Check if a user already exists by username or email"""
    users = read_users()
    for user in users:
        if user['username'] == username or user['email'] == email:
            return True
    return False


def register_user(username, email, password):
    """Register a new user"""
    users = read_users()
    users.append({"username": username, "email": email, "password": password, "role": "user"})
    write_users(users)


def authenticate_user(email, password):
    """Authenticate user login"""
    users = read_users()
    for user in users:
        if user['email'] == email and user['password'] == password:
            return user
    return None


def update_user_info(email, new_data):
    """Update user's information"""
    users = read_users()
    for user in users:
        if user['email'] == email:
            for key, value in new_data.items():
                user[key] = value
            write_users(users)
            return user
    return None
