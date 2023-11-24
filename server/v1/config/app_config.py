from flask_cors import CORS
from flask import Blueprint, Flask
from typing import Any
from flask_socketio import SocketIO

from server.v1.api.client.routes.auth.auth_route import auth_route
from flask_cors import CORS
from server.v1.api.client.routes.tool.tool_route import tool_route
from server.v1.api.admin.routes.user.user import user_route
from server.v1.api.test.test_route import test_route
from server.v1.api.utils.server_env import get_env
from tools.Tool import Tool
from server.v1.api.client.socket.events import init_socket_events
# from gevent import monkey
# monkey.patch_all()

# print(get_env('ALLOWED_ORIGINS').split(','))

APP_CONFIG: dict[str, Any] = {
    "ALLOWED_ORIGINS": get_env('ALLOWED_ORIGINS').split(',')
    # "ALLOWED_ORIGINS": '*'
}


tool_storage_path: str = Tool.storage_path

def get_app_config(key: str) -> Any:
    value = APP_CONFIG[key]
    if (not value):
        raise Exception(f"APP_CONFIG with key {key} is not exists")
    return value

def config_app(app: Flask) -> None:
    CORS(app, origins=get_app_config("ALLOWED_ORIGINS"),  supports_credentials=True)

    # apiPrefix = '/api' if get_env('ENVIRONMENT') == 'development' else ''
    apiPrefix = '/api'
    client_route = Blueprint("client", __name__, url_prefix=apiPrefix + "/v1/client")
    client_route.register_blueprint(auth_route)
    client_route.register_blueprint(tool_route)

    admin_route = Blueprint("admin", __name__, url_prefix=apiPrefix + "/v1/admin")
    admin_route.register_blueprint(user_route)

    test = Blueprint('test', __name__, url_prefix=apiPrefix + '/v1/test')
    test.register_blueprint(test_route)

    app.register_blueprint(client_route)
    app.register_blueprint(admin_route)
    app.register_blueprint(test)

    # routes = []
    # for rule in app.url_map.iter_rules():
    #     methods = rule.methods
    #     routes.append(f"{methods} {rule.rule}")

    # print("\n".join(sorted(routes)))



def get_socket(app: Flask) -> SocketIO:
    PORT: int = int(get_env("PORT"))
    socketio = SocketIO(
        app,
        debug=(get_env("ENVIRONMENT") == "development"),
        port=PORT,
        host="0.0.0.0",
        cors_allowed_origins=get_app_config("ALLOWED_ORIGINS"),
        # async_mode="threading"
        # host="0.0.0.0"
    )
    init_socket_events(socketio)
    return socketio
