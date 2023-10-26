from typing import Any
from flask import Blueprint, Response, jsonify, request
from datetime import datetime
import uuid
from server.v1.api.client.models.user_collection import UserDoc, username_exists
from server.v1.api.utils.StatusCode import StatusCode

signup_route = Blueprint("signup", __name__, url_prefix="/signup")

@signup_route.post("")
def handle_signup() -> tuple[Response, int] | Response:
    data: Any | None = request.json
    if data is None:
        return jsonify({"message": "Invalid JSON data"}), StatusCode.BadRequest.value

    username = data.get('username')
    current_time: datetime = datetime.utcnow()

    # Check if username already exists in the collection
    if username_exists(username):
        return jsonify({"message": "Username already exists"}), StatusCode.Conflict.value

    # FlaskLog.info(f"role = {data.get('role')}")
    # Insert user_data into MongoDB
    new_user: UserDoc = UserDoc(
        id=str(uuid.uuid4()),
        name=data.get('name'),
        username=username,
        password=data.get('password'),
        email=data.get('email'),
        role=data.get("role")
    ).save()

    response_data = {
        "message": "Sign Up successful",
        "_id": new_user.id,
        "name": new_user.name,
        "username": username,
        "password": new_user.password,
        "email": new_user.email,
        "email_verified": False,
        "last_online": current_time,
        "created_at": current_time,
        "last_modified_at": current_time
    }

    return jsonify(response_data)
