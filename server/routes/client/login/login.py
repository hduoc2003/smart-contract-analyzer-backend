from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import datetime
from flask_cors import CORS, cross_origin


login_route = Blueprint("login", __name__, url_prefix="/login")

load_dotenv()
CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
DATABASE_NAME = "TOOL"
client = MongoClient(CONNECTION_STRING)
db = client['TOOL']  # Replace with your database name
collection = db['USERS']  # Replace with your collection name
users_DB = collection['USERS']  # Replace with yo

@login_route.route("/", methods=['POST'])
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
        return jsonify({"message": "Username not exists"}), 409
    else:
        if (existing_user['password'] != password):
            return jsonify({"message": "Wrong password"})
        else:
            return jsonify({"message": "Login success"})