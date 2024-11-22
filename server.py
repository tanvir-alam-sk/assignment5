from flask import Flask;
from flask import jsonify;
from flask import request;
import os
import json

app=Flask(__name__);

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


#  delete-user route

@app.route('/destination/<id>', methods=['DELETE'])
def delete_destination(id):

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
    app.run(debug=True,port=5000)