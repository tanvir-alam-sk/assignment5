from flask import Flask;
from flask import jsonify;
from flask import request;
from flasgger import Swagger 
import os
import json
from utility.jwt import verify_token
from db.token import jwt_token

app=Flask(__name__);
swagger = Swagger(app)


user_file_path = os.path.join("db", "users.py")

# Function to read users from file
def read_users():
    with open(user_file_path, "r") as file:
        return json.load(file)
    


destination_file_path = os.path.join("db", "destination.py");


# Ensure the file exists
if not os.path.exists(destination_file_path):
    with open("destination_file_path", "w") as file:
        json.dump([], file)


# Function to read destination from file
def read_destination():
    with open(destination_file_path, "r") as file:
        return json.load(file)


# Function to write destination to file
def write_destination(destination):
    with open(destination_file_path, "w") as file:
        json.dump(destination, file, indent=4)



@app.route("/", methods=["GET"])
def home():
    """
    Home Page
    ---
    tags:
      - General
    responses:
      200:
        description: Welcome message
        schema:
          type: string
          example: "Welcome destination"
    """
    return "Welcome destination"

#  get destination

@app.route("/destination", methods=["GET"])
def get_destination():
    """
    Retrieve Destination Information
    ---
    tags:
      - Destination
    responses:
      200:
        description: Successfully retrieved the destination data
        schema:
          type: object
          properties:
            Id:
              type: integer
              example: 99997
            Name:
              type: string
              example: "Grand Canyon"
            Description:
              type: string
              example: "A massive natural wonder in the USA, renowned for its stunning landscapes, hiking trails, and geological formations."
            Location:
              type: string
              example: "USA"
      500:
        description: Internal Server Error (e.g., file not found or unreadable)
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Unable to load destination data"
    """
    try:
        destination = read_destination()
        return jsonify(destination), 200
    except Exception as e:
        return jsonify({"error": "Unable to load destination data"}), 500

# add distination
@app.route('/destination', methods=['POST'])
def add_destination():
    """
    Add a new destination
    ---
    tags:
      - Destination
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
            Id:
              type: integer
              description: Unique identifier for the destination
              example: 99997
            Name:
              type: string
              description: Name of the destination
              example: Grand Canyon
            Description:
              type: string
              description: Detailed description of the destination
              example: "A massive natural wonder in the USA, renowned for its stunning landscapes, hiking trails, and geological formations."
            Location:
              type: string
              description: Geographical location of the destination
              example: "USA"
    responses:
      201:
        description: Destination added successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Destination Add successfully"
      400:
        description: Bad request (missing or invalid data)
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Id, Location, Description and Location are required"
      401:
        description: Unauthorized access (user not found or not admin)
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Unauthorized Access"
      403:
        description: Forbidden access (only admins can add destinations)
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Forbidden Access"
      409:
        description: Conflict (duplicate Id)
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Id already taken please provide unique id"
    """
    jwt_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    logined_user_email = verify_token(jwt_token)

    if not logined_user_email:
        return jsonify({"message": "Unauthorized Access"}), 401

    users = read_users()
    find_user = -1

    for user in users:
        if user['email'] == logined_user_email:
            if user['role'] == "admin":
                find_user = 1
            else:
                return jsonify({"error": "Forbidden Access"}), 403

    if find_user == -1:
        return jsonify({"message": "Unauthorized Access"}), 401

    destinations = read_destination()

    data = request.get_json()

    # Validate input
    Id = data.get('Id')
    Name = data.get('Name')
    Description = data.get('Description')
    Location = data.get('Location')

    if not Id or not Name or not Description or not Location:
        return jsonify({"error": "Id, Location, Description and Location are required"}), 400

    # Check if the Id already exists
    for destination in destinations:
        if destination['Id'] == Id:
            return jsonify({"error": "Id already taken please provide unique id"}), 409

    # Add the new destination
    destinations.append({"Id": Id, "Name": Name, "Description": Description, "Location": Location})
    write_destination(destinations)

    return jsonify({"message": "Destination Add successfully"}), 201



#  delete-user route

@app.route('/destination/<id>', methods=['DELETE'])
def delete_destination(id):
    """
    Delete a destination
    ---
    tags:
      - Destination
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: JWT token for user authentication
        example: "Bearer <your_token>"
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the destination to delete
        example: 99997
    responses:
      200:
        description: Destination deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Destination deleted successfully"
      400:
        description: Bad request (invalid or missing ID)
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid ID provided"
      401:
        description: Unauthorized access (user not found or not admin)
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Unauthorized Access"
      403:
        description: Forbidden access (only admins can delete destinations)
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Forbidden Access"
      404:
        description: Not found (destination does not exist)
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Destination not found"
    """
    jwt_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    logined_user_email = verify_token(jwt_token)

    if not logined_user_email:
        return jsonify({"message": "Unauthorized Access"}), 401

    users = read_users()
    find_user = -1

    for user in users:
        if user['email'] == logined_user_email:
            if user['role'] == "admin":
                find_user = 1
            else:
                return jsonify({"error": "Forbidden Access"}), 403

    if find_user == -1:
        return jsonify({"message": "Unauthorized Access"}), 401

    destinations = read_destination()

    # Find the destination to delete by id
    destination_to_delete = None
    for destination in destinations:
        if destination['Id'] == int(id):
            destination_to_delete = destination
            break

    # If destination is not found, return an error
    if not destination_to_delete:
        return jsonify({"error": "Destination not found"}), 404

    # Remove the destination from the list
    destinations.remove(destination_to_delete)

    # Write the updated list of destinations to the file
    write_destination(destinations)

    return jsonify({"message": "Destination deleted successfully"}), 200





if __name__== "__main__":
    app.run(debug=True,port=5002)