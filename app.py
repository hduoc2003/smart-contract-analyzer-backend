from flask import Flask, render_template, make_response, jsonify, request
from server.routes.client.login.login import login_route
from server.routes.client.signup.signup import signup_route
from server.routes.client.tool.tool import tool_route
from server.routes.admin.user.user import user_route
from server.config.corsOptions import setup_app_config
from server.routes.api.auth import auth_bp
from server.config.dbConnection import connect_to_database
from flask_cors import CORS, cross_origin
import logging
import datetime
import uuid
import sys
import os
from dotenv import load_dotenv
logging.basicConfig(level=logging.INFO)

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

load_dotenv()
PORT = int(os.getenv("PORT") or 5000)

#NOTE: Đổi từ pymongo qua dùng mongoengine nhé
connect_to_database()

app = Flask(__name__)

setup_app_config(app)

#đưa chia route vào file riêng route/api/auth_bp và các route khác
app.register_blueprint(auth_bp)
@app.route("/")
@cross_origin()
def home():
    logging.info("get home page")
    return render_template('home.html')

# @app.route("/login", methods=['POST'])
# @cross_origin()
# def login():
#     data = request.json
#     if data is None:
#         return jsonify({"message": "Invalid JSON data"}), 400

#     username = data.get('username')
#     password = data.get('password')

#     existing_user = collection.find_one({"username": username})
#     # return jsonify(existing_user)
#     if not existing_user:
#         return jsonify({"message": "Username not exists"}), 200
#     else:
#         if (existing_user['password'] != password):
#             return jsonify({"message": "Wrong password"})
#         else:
#             return jsonify({"message": "Login success"})

# @app.route("/signup", methods=['POST'])
# @cross_origin()
# def signup():
#     data = request.json
#     if data is None:
#         return jsonify({"message": "Invalid JSON data"}), 400

#     user_id = str(uuid.uuid4())
#     name = data.get('name')
#     email = data.get('email')
#     username = data.get('username')
#     password = data.get('password')
#     current_time = datetime.datetime.utcnow()

#     user_data = {
#         "_id": user_id,
#         "name": name,
#         "username": username,
#         "password": password,
#         "email": email,
#         "email_verified": False,
#         "last_online": current_time,
#         "created_at": current_time,
#         "last_modified_at": current_time
#     }

#     # Check if username already exists in the collection
#     existing_user = collection.find_one({"username": username})
#     if existing_user:
#         return jsonify({"message": "Username already exists"}), 409
#     # Insert user_data into MongoDB
#     result = collection.insert_one(user_data)

#     response_data = {
#         "message": "Sign Up successful",
#         "_id": user_id,
#         "name": name,
#         "username": username,
#         "password": password,
#         "email": email,
#         "email_verified": False,
#         "last_online": current_time,
#         "created_at": current_time,
#         "last_modified_at": current_time,
#         "inserted_id": str(result.inserted_id)
#     }

#     return jsonify(response_data)

if __name__ == "__main__":
    app.run(debug=True, port=PORT)
