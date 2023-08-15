from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import datetime
import uuid
import os

signup_route = Blueprint("signup", __name__, url_prefix="/signup")
load_dotenv()
CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
DATABASE_NAME = "TOOL"
client = MongoClient(CONNECTION_STRING)
db = client['TOOL']  # Replace with your database name
collection = db['USERS']  # Replace with your collection name
users_DB = collection['USERS']  # Replace with yo


@signup_route.route("/", methods=['POST'])
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
