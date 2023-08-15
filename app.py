from flask import Flask, render_template, make_response, jsonify, request
from pymongo import MongoClient
from server.routes.client.login.login import login_route
from server.routes.client.signup.signup import signup_route
from server.routes.client.tool.tool import tool_route
from server.routes.admin.user.user import user_route
from flask_cors import CORS, cross_origin

import datetime
import uuid
import sys
import os
from dotenv import load_dotenv
from flask_pymongo import PyMongo

load_dotenv()
CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
DATABASE_NAME = "TOOL"
client = MongoClient(CONNECTION_STRING)
db = client['TOOL']
collection = db['USERS']
users_DB = collection['USERS']

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def setup_app_config(app):
    CORS(app, resources={r"/*": {"origins": "*"}},  supports_credentials=True)

load_dotenv()
PORT = int(os.getenv("PORT") or 5000)

app = Flask(__name__)

setup_app_config(app)
# app.register_blueprint(user_route)
# app.register_blueprint(login_route)
# app.register_blueprint(signup_route)
# app.register_blueprint(tool_route)

@app.route("/")
@cross_origin()
def home():
    return render_template('home.html')

@app.route("/login", methods=['POST'])
@cross_origin()
def login():
    data = request.json
    if data is None:
        return jsonify({"message": "Invalid JSON data"}), 400

    username = data.get('username')
    password = data.get('password')

    existing_user = collection.find_one({"username": username})
    # return jsonify(existing_user)
    if not existing_user:
        return jsonify({"message": "Username not exists"}), 200
    else:
        if (existing_user['password'] != password):
            return jsonify({"message": "Wrong password"})
        else:
            return jsonify({"message": "Login success"})

@app.route("/signup", methods=['POST'])
@cross_origin()
def signup():
    data = request.json
    if data is None:
        return jsonify({"message": "Invalid JSON data"}), 400

    user_id = str(uuid.uuid4())
    name = data.get('name')
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    current_time = datetime.datetime.utcnow()

    user_data = {
        "_id": user_id,
        "name": name,
        "username": username,
        "password": password,
        "email": email,
        "email_verified": False,
        "last_online": current_time,
        "created_at": current_time,
        "last_modified_at": current_time
    }

    # Check if username already exists in the collection
    existing_user = collection.find_one({"username": username})
    if existing_user:
        return jsonify({"message": "Username already exists"}), 409
    # Insert user_data into MongoDB
    result = collection.insert_one(user_data)

    response_data = {
        "message": "Sign Up successful",
        "_id": user_id,
        "name": name,
        "username": username,
        "password": password,
        "email": email,
        "email_verified": False,
        "last_online": current_time,
        "created_at": current_time,
        "last_modified_at": current_time,
        "inserted_id": str(result.inserted_id)
    }

    return jsonify(response_data)

if __name__ == "__main__":
    app.run(debug=True, port=PORT)
import sys
import os
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask
from server.route.login.login import login_route
from server.route.signup.signup import signup_route
from server.route.tool.tool import tool_route

load_dotenv()
PORT = int(os.getenv("PORT") or 5000)

app = Flask(__name__)
app.register_blueprint(login_route)
app.register_blueprint(signup_route)
app.register_blueprint(tool_route)

@app.route("/")
def response():
    return "hello"

if __name__ == "__main__":
    app.run(debug=True, port=PORT)
