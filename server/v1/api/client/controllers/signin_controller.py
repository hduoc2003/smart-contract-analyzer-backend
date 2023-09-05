from typing import Any

import logging
import flask_pyjwt
from flask import Blueprint, request, jsonify, current_app, make_response
from flask_bcrypt import Bcrypt
from server.v1.api.client.models.users_collection import UserDoc

from server.v1.api.utils.FlaskLog import FlaskLog
from server.v1.api.utils.StatusCode import StatusCode
bcrypt = Bcrypt()

#set để dùng ưu tiên logging.info
logging.basicConfig(level=logging.INFO)

def generate_token():
    # You can use any method to generate a token (JWT, session, etc.)
    # For simplicity, we'll return a dummy token here
    return # In a real application, you'd use a library like PyJWT

def handle_login():
    logging.info("Received a POST request to login")
    data: Any | None = request.json
    
    # FlaskLog.info(data)
    if data is None:
        return jsonify({"message": "Invalid JSON data"}), StatusCode.BadRequest.value

    data = request.get_json()
    username = data.get('username') #type: ignore
    password = data.get('password') #type: ignore
    if not username or not password:
        logging.error(f'No {username} or {password}')
        return jsonify({'message': 'Missing email or password'}), StatusCode.BadRequest.value
    
    user = UserDoc.get_field_value(username, "username")
    if user is None:
        logging.error(f"No {username} username in DB")
        return jsonify({'message': 'No username found, please sign up or contact the admin'}), StatusCode.NotFound.value

    #TODO: Làm JWT ở đây
    if user and bcrypt.check_password_hash(user.password, password):
        token = generate_token()
        UserDoc.update_last_online(username)
        return jsonify({"message": "Login successful", "token": token}), StatusCode.OK.value

    return jsonify({"message": "Invalid credentials"}), StatusCode.NotFound.value
    
    
