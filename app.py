from dotenv import load_dotenv
from flask_socketio import SocketIO

load_dotenv()
from server.v1.config.database_config import init_database
init_database()
from flask import Flask
from server.v1.config.app_config import setup_app_config

from server.v1.api.utils.server_env import get_env

app = Flask(__name__)
setup_app_config(app)

import server.v1.api.client.socket.events
from server.v1.config.app_config import socketio

if __name__ == "__main__":
    socketio.run(app, use_reloader=True, log_output=True)
