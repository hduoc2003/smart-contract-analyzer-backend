from flask_socketio import SocketIO
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from server.v1.api.utils.server_env import get_env

from dotenv import find_dotenv, load_dotenv
dotenv_file = find_dotenv('.env.development')
load_dotenv(dotenv_file if len(dotenv_file) > 0 else find_dotenv('.env.production'))

from server.v1.config.database_config import init_database
init_database()
from flask import Flask
from server.v1.config.app_config import config_app, get_socket

app = Flask(__name__)
config_app(app)
socketio: SocketIO = get_socket(app)

def start_server() -> None:

    app.run(
        port=int(get_env("PORT")),
        host="0.0.0.0",
        debug=(get_env("ENVIRONMENT") == "development")
    )
    # socketio.run(app, use_reloader=True, log_output=True)

if __name__ == "__main__":
    start_server()

