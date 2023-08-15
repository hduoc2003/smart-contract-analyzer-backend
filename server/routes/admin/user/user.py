from flask import Blueprint, Flask, request, jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import os
import sys

load_dotenv()
CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
DATABASE_NAME = "TOOL"

user_route = Blueprint("user", __name__, url_prefix="/user")
# MongoDB connection
# Replace with your MongoDB connection URL
client = MongoClient(
    'mongodb+srv://shodydosh:dT8NJQfeB25rAtj@cluster0.l96vywb.mongodb.net/?retryWrites=true&w=majority')
db = client['TOOL']  # Replace with your database name
collection = db['USERS']  # Replace with your collection name


@user_route.route("/", methods=["GET"])
def get_all_users():
    try:
        query = {}  # Your query goes here
        result = collection.find(query)
        data = [item for item in result]
        return jsonify(data)
    except Exception as e:
        return str(e), 500


@user_route.route("/<string:user_id>", methods=["GET"])
def search_user(user_id):
    try:
        query = {'_id': user_id}
        user = collection.find_one(query)

        if user:
            user['_id'] = str(user['_id'])
            return jsonify(user)
        else:
            return jsonify({'message': 'User not found', 'user_id': user_id}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@user_route.route('/delete/<string:user_id>', methods=["DELETE"])
def delete_user(user_id):
    try:
        query = {'_id': user_id}
        user = collection.find_one(query)

        if user:
            collection.delete_one(query)
            return jsonify({'message': 'User deleted successfully'}), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@user_route.route('/update/<string:user_id>', methods=["PUT"])
def update_user(user_id):
    try:
        query = {'_id': user_id}
        user = collection.find_one(query)

        if user:
            # Assuming you have a JSON payload with updated user data
            updated_data = request.get_json()  # Make sure to import 'request' from Flask
            collection.update_one(query, {'$set': updated_data})
            return jsonify({'message': 'User updated successfully'}), 200
        else:
            return jsonify({'message': 'User not found'}), 404

    except Exception as e:
        return jsonify({'message': str(e)}), 500
