from flask import Blueprint
from server.v1.api.client.routes.tool.submit.submit_route import submit_route
from server.v1.api.client.routes.tool.file.file_route import file_route

tool_route = Blueprint("tool_bp", __name__, url_prefix="/tool")
tool_route.register_blueprint(submit_route)
tool_route.register_blueprint(file_route)

