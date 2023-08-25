from flask import Blueprint, jsonify
from server.controllers.auth_controller import handle_login, handle_signup

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")
auth_bp.route("/login", methods=["POST", "OPTIONS"])(handle_login)
auth_bp.route("/logout", methods=["POST"])(handle_signup)