from typing import Any
from flask import Blueprint, Response, jsonify, request
from datetime import datetime
import uuid
from server.v1.api.client.models.user_collection import *
from server.v1.api.utils.StatusCode import StatusCode

def handle_signup() -> tuple[Response, int] | Response:
    data: Any = request.json
    if not validate_json_data(data):
        return jsonify({"message": "Invalid JSON data"}), StatusCode.BadRequest.value

    username = data.get('username')

    if username_exists(username):
        return jsonify({"message": "Username already exists"}), StatusCode.Conflict.value

    new_user = create_new_user(data, username)
    current_time: datetime = datetime.utcnow()
    response_data = format_sign_up_response(new_user, username, current_time)

    return jsonify(response_data)

def validate_json_data(data: Any) -> bool:
    return data is not None



