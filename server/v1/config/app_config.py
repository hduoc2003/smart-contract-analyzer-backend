from flask_cors import CORS, cross_origin
from flask import Blueprint, Flask
from typing import Any


from server.v1.api.client.routes.auth_route import auth_route
from flask_cors import CORS
from server.v1.api.client.routes.tool_route import tool_route
from server.v1.api.admin.routes.user.user import user_route
import tools.Tool
APP_CONFIG: dict[str, Any] = {
    "ALLOWED_ORIGINS": ["http://localhost:3000"]
}
storage_path: str = tools.Tool.Tool.storage_path

def get_app_config(key: str) -> Any:
    value = APP_CONFIG[key]
    if (not value):
        raise Exception(f"APP_CONFIG with key {key} is not exists")
    return value

def setup_app_config(app: Flask):
    CORS(app, origins=get_app_config("ALLOWED_ORIGINS"),  supports_credentials=True)

    #stop automate sorting dict response
    app.json.sort_keys = False
    app.register_blueprint(auth_route)
    app.register_blueprint(tool_route)
    app.register_blueprint(user_route)

def get_local_storage_path():
    return storage_path