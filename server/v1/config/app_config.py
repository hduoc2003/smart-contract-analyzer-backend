from flask_cors import CORS
from flask import Blueprint, Flask
from typing import Any
from flask_session import Session

from server.v1.api.client.routes.auth_route import auth_route
from flask_cors import CORS
from server.v1.api.client.routes.tool_route import tool_route
from server.v1.api.admin.routes.user.user import user_route
import tools.Tool
from datetime import timedelta
APP_CONFIG: dict[str, Any] = {
    "ALLOWED_ORIGINS": ["http://localhost:3000"]
}

tool_storage_path: str = tools.Tool.Tool.storage_path

def get_app_config(key: str) -> Any:
    value = APP_CONFIG[key]
    if (not value):
        raise Exception(f"APP_CONFIG with key {key} is not exists")
    return value

def setup_app_config(app: Flask) -> None:
    CORS(app, origins=get_app_config("ALLOWED_ORIGINS"),  supports_credentials=True)
    app.secret_key = "Can't be hack Password"
    app.config['SESSION_TYPE'] = 'filesystem'  # You can choose a different backend
    app.permanent_session_lifetime= timedelta(days=5)
    app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)
    Session(app)

    #stop automate sorting dict response
    app.json.sort_keys = False # type: ignore

    client_route = Blueprint("client", __name__, url_prefix="/api/v1/client")
    client_route.register_blueprint(auth_route)
    client_route.register_blueprint(tool_route)

    admin_route = Blueprint("admin", __name__, url_prefix="/api/v1/admin")
    admin_route.register_blueprint(user_route)

    app.register_blueprint(client_route)
    app.register_blueprint(admin_route)

