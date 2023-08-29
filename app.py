import sys
import os
from dotenv import load_dotenv

from flask import Flask
from server.v1.api.utils.server_env import get_env
from server.v1.config.database_config import init_database
from server.v1.config.app_config import setup_app_config

load_dotenv()
app = Flask(__name__)
init_database()
setup_app_config(app)

if __name__ == "__main__":
    PORT: int = int(get_env("PORT"))
    app.run(debug=(get_env("ENVIRONMENT") == "development"), port=PORT)