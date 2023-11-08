from flask import Blueprint
from server.v1.api.client.controllers.auth.signin_controller import handle_signin
from server.v1.api.client.controllers.auth.signup_controller import handle_signup

auth_route = Blueprint("auth_bp", __name__, url_prefix="/auth")
auth_route.route("/login", methods=["POST"])(handle_signin)
auth_route.route("/signup", methods=["POST"])(handle_signup)
