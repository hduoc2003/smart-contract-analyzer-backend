import logging
import flask_pyjwt
from flask import Blueprint, request, jsonify, current_app
from flask_bcrypt import Bcrypt
from server.models.user import User
from server.utils.user_activity import get_field_value, update_last_online
auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

auth_bp.route('/login', method=['POST'])

#set để dùng ưu tiên logging.info
logging.basicConfig(level=logging.INFO)

# def verify_email(email):
#     email = User.objects(email=email).first()
#     if email:
#         return True
#     return False
def handle_signup():
    logging.info("Received a POST request to /your_post_route")
    return jsonify({"message": "Signup successful"})

def handle_login():
    logging.info("Received a POST request to /your_post_route")

    data = request.get_json()
    username = data.get('email')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Missing email or password'}), 400
    
    
    user = get_field_value(username, "username")
    if (user is None):
        logging.error(f"No {username} username in DB")
        return jsonify({'message': 'No username found, please sign up or contact the admin'}), 401

    #TODO: Làm JWT ở đây
    if user and bcrypt.check_password_hash(user.password, password):
        token = generate_token()
    update_last_online(username)
    get_field_value(username, "created_at")
    
    return  jsonify({"message": "Login successful"})

    
    
def generate_token():
    # You can use any method to generate a token (JWT, session, etc.)
    # For simplicity, we'll return a dummy token here
    return # In a real application, you'd use a library like PyJWT

