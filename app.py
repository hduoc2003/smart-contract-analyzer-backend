import sys
import os

from server.v1.config.database_config import init_database
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from server.v1.api.utils.server_env import get_env
from server.v1.config.app_config import setup_app_config

app = Flask(__name__)
init_database()
setup_app_config(app)

if __name__ == "__main__":
    PORT: int = int(get_env("PORT"))
    app.run(debug=(get_env("ENVIRONMENT") == "development"), port=PORT)
