from dotenv import load_dotenv

load_dotenv()
from server.v1.config.database_config import init_database
init_database()
from flask import Flask
from server.v1.config.app_config import setup_app_config

from server.v1.api.utils.server_env import get_env

app = Flask(__name__)
setup_app_config(app)

if __name__ == "__main__":
    PORT: int = int(get_env("PORT"))
    app.run(debug=(get_env("ENVIRONMENT") == "development"), port=PORT)
