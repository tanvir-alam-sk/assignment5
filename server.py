from flask import Flask;
from flask import jsonify;
from flask import request;
import os
import json
from utility.jwt import verify_token
from db.token import jwt_token

app=Flask(__name__);


user_file_path = os.path.join("db", "users.py")
# Function to read users from file
def read_users():
    with open(user_file_path, "r") as file:
        return json.load(file)
    

@app.route("/",methods=["GET"])
def home():
    return "Welcome destination"


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


#  get destination

@app.route("/destination",methods=["GET"])
def get_destination():
    destination=read_destination();
    return destination


# add distination
@app.route('/destination', methods=['POST'])
def add_destination():

    logined_user_email=verify_token(jwt_token)
    print(logined_user_email)
    users = read_users()
    find_user=-1

    for user in users:
        if((user['email'] == logined_user_email)):
            # find_user=0
            if(user['role'] == "admin"):
                find_user=1
            else:
                return jsonify({"error": "Forbidden Access"}), 403
        
    if(find_user==-1):
        return jsonify({"message": "Unauthorized Access"}), 401

    # Read existing users
    destinations = read_destination();

    data = request.get_json()


    # Validate input
    Id = data.get('Id')
    Location = data.get('Name')
    Description=data.get('Description')
    Location = data.get('Location')
    
    if not Id or not Location or not Description or not Location:
        return jsonify({"error": "Id, Location, Description and Location are required"}), 400
    
    for destination in destinations:
        if(destination['Id'] == Id):
            return jsonify({"error": "Id already taken please provide unique id"}), 400

    # Add the new user
    destinations.append({"Id": Id,"Location":Location, "Description": Description,"Location":Location})
    write_destination(destinations)

    return jsonify({"message": "Destination Add successfully"}), 201



#  delete-user route

@app.route('/destination/<id>', methods=['DELETE'])
def delete_destination(id):

    logined_user_email=verify_token(jwt_token)
    users = read_users()
    find_user=-1

    for user in users:
        if((user['email'] == logined_user_email)):
            # find_user=0
            if(user['role'] == "admin"):
                find_user=1
            else:
                return jsonify({"error": "Forbidden Access"}), 403
        
    if(find_user==-1):
        return jsonify({"message": "Unauthorized Access"}), 401

    # Read existing users
    destinations = read_destination();
    

    # Find the destination to delete by id
    destination_to_delete = None;
    for destination in destinations:
        if (destination['Id'] == int(id)):
            destination_to_delete = destination
            break


    # If destination is not found, return an error
    if not destination_to_delete:
        return jsonify({"error": "Destination not found"}), 404

    # Remove the destination from the list
    destinations.remove(destination_to_delete)
    
    # Write the updated list of destination to the file
    write_destination(destinations)

    return jsonify({"message": "Destination deleted successfully"}), 200





if __name__== "__main__":
    app.run(debug=True,port=5002)