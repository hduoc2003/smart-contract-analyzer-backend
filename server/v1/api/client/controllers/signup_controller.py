from typing import Any
from flask import Blueprint, Response, jsonify, request
from datetime import datetime
import uuid
from server.v1.api.client.models.users_collection import UserDoc
from server.v1.api.utils.StatusCode import StatusCode

signup_route = Blueprint("signup", __name__, url_prefix="/signup")

def validate_json_data(data: Any) -> bool:
    return data is not None

def check_username_exists(username: str) -> bool:
    return UserDoc.username_exists(username)

def create_new_user(data: Any, username: str) -> UserDoc:
    current_time: datetime = datetime.utcnow()
    new_user = UserDoc(
        id=str(uuid.uuid4()),
        name=data.get('name'),
        username=username,
        password=data.get('password'),
        email=data.get('email'),
        role=data.get("role")
    ).save()
    return new_user

def format_response(new_user: UserDoc, username: str, current_time: datetime) -> dict:
    return {
        "message": "Sign Up successful",
        "_id": new_user.id,
        "name": new_user.name,
        "username": username,
        "password": new_user.password,
        "email": new_user.email,
        "email_verified": False,
        "last_online": current_time,
        "created_at": current_time,
        "last_modified_at": current_time  # TODO: Not current time
    }

def handle_signup() -> tuple[Response, int] | Response:
    data: Any = request.json
    if not validate_json_data(data):
        return jsonify({"message": "Invalid JSON data"}), StatusCode.BadRequest.value

    username = data.get('username')

    if check_username_exists(username):
        return jsonify({"message": "Username already exists"}), StatusCode.Conflict.value

    new_user = create_new_user(data, username)
    current_time = datetime.utcnow()
    response_data = format_response(new_user, username, current_time)

    return jsonify(response_data)
