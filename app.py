from flask import Flask;
from flask import jsonify;
from flask import request;

app=Flask(__name__);

@app.route("/",methods=["GET"])
def home1():
    print("hallo world2");
    return "Hallo World114"


@app.route("/user",methods=["get"])
def get_user():
    return "get user"



@app.route("/user",methods=["POST"])
def post_user():
    data=request.get_json()
    print(data);




if __name__== "__main__":
    app.run(debug=True)