from typing import Any

from flask import Blueprint, Flask
from server.v1.api.client.routes.login.login import login_route
from server.v1.api.client.routes.signup.signup import signup_route
from flask_cors import CORS
from server.v1.api.client.routes.tool.tool import tool_route
from server.v1.api.admin.routes.user.user import user_route


APP_CONFIG: dict[str, Any] = {
    "ALLOWED_ORIGINS": ["http://localhost:3000"]
}

def get_app_config(key: str) -> Any:
    value = APP_CONFIG[key]
    if (not value):
        raise Exception(f"APP_CONFIG with key {key} is not exists")
    return value

def setup_app_config(app: Flask) -> None:

    # routes config
    CORS(app, origins=get_app_config("ALLOWED_ORIGINS"),  supports_credentials=True)

    # client_route = Blueprint("client", __name__, url_prefix="/api/v1/client")
    # client_route.register_blueprint(login_route)
    # client_route.register_blueprint(signup_route)
    # client_route.register_blueprint(tool_route)

    # admin_route = Blueprint("admin", __name__, url_prefix="/api/v1/admin")
    # admin_route.register_blueprint(user_route)

    # app.register_blueprint(client_route)
    # app.register_blueprint(admin_route)

    app.register_blueprint(login_route)
    app.register_blueprint(signup_route)
    app.register_blueprint(tool_route)
    app.register_blueprint(user_route)
