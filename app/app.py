from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())
from server.v1.config.database_config import init_database
init_database()
from flask import Flask, url_for, send_from_directory,render_template
from server.v1.config.app_config import setup_app_config

from server.v1.api.utils.server_env import get_env

app = Flask(__name__)
    
# app = Flask(__name__, static_folder="build")

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')  
# def serve(path):
#     print (app.static_folder+ '/' + path)
#     if path != "" and os.path.exists(app.static_folder + '/' + path ):
#         print("WTH")
#         return send_from_directory(app.static_folder, path, max_age=0)
#     print("WTF")
#     return send_from_directory(app.static_folder, 'index1.html', max_age=0), 404
setup_app_config(app)



import server.v1.api.client.socket.events
from server.v1.config.app_config import socketio

if __name__ == "__main__":
    socketio.run(app, use_reloader=True, log_output=True)
