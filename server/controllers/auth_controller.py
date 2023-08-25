import logging
import flask_pyjwt
from flask import Blueprint, request, jsonify, current_app, make_response
from flask_bcrypt import Bcrypt
from server.models.user import User
from server.utils.user_activity import get_field_value, update_last_online
bcrypt = Bcrypt()

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

    if request.method == "OPTIONS": # CORS preflight
        logging.info("Option handling")
        # return _build_cors_preflight_response()
        return jsonify({"message":"OPTIONS"})
    elif request.method == "POST": 
        logging.info("Received a POST request to /your_post_route")

        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            logging.error(f'No {username} or {password}')
            return jsonify({'message': 'Missing email or password'}), 400
        
        user = get_field_value(username, "username")
        if (user is None):
            logging.error(f"No {username} username in DB")
            return jsonify({'message': 'No username found, please sign up or contact the admin'}), 401
        print("pass user in DB check")
        #TODO: Làm JWT ở đây
        if user and bcrypt.check_password_hash(user.password, password):
            token = generate_token()
        update_last_online(username)
        get_field_value(username, "created_at")
        
        return  _corsify_actual_response(jsonify({"message": "Login successful"})), 200
    return jsonify({"message": "WTF"})
    
    
def generate_token():
    # You can use any method to generate a token (JWT, session, etc.)
    # For simplicity, we'll return a dummy token here
    return # In a real application, you'd use a library like PyJWT

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response