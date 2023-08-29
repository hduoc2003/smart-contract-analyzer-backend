from typing import Any
from flask import Blueprint, Response, jsonify, request
from server.v1.api.client.models.users_collection import UserDoc
from server.v1.api.utils.FlaskLog import FlaskLog

from server.v1.api.utils.StatusCode import StatusCode

login_route = Blueprint("login", __name__, url_prefix="/login")

@login_route.post("")
def handle_login() -> tuple[Response, int] | Response:
    data: Any | None = request.json
    # FlaskLog.info(data)
    if data is None:
        return jsonify({"message": "Invalid JSON data"}), StatusCode.BadRequest.value

    username = data.get('username')
    password = data.get('password')

    existing_user: UserDoc = UserDoc.objects(username=username).first()
    if not existing_user:
        return jsonify({"message": "Username not exists"}), StatusCode.Conflict.value
    else:
        if (existing_user.password != password):
            return jsonify({"message": "Wrong password"})
        else:
            return jsonify({"message": "Login success"})
