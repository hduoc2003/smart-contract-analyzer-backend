from typing import Any

import logging
from flask import request, jsonify
from flask_bcrypt import Bcrypt
from server.v1.api.client.models.user_collection import *
from server.v1.api.utils.StatusCode import StatusCode
bcrypt = Bcrypt()

def handle_signin():
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

    user = get_field_value(username, "username")
    if user is None:
        logging.error(f"No {username} username in DB")
        return jsonify({'message': 'No username found, please sign up or contact the admin'}), StatusCode.NotFound.value

    return jsonify({"message": "Invalid credentials"}), StatusCode.NotFound.value


