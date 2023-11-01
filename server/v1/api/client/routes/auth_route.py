from flask import Blueprint, jsonify
from server.v1.api.client.controllers.signin_controller import handle_login
from server.v1.api.client.controllers.signup_controller import handle_signup

auth_route = Blueprint("auth_bp", __name__, url_prefix="/auth")
auth_route.route("/login", methods=["POST"])(handle_login)
auth_route.route("/signup", methods=["POST"])(handle_signup)