from flask import Blueprint
from server.v1.api.client.controllers.tool_controller import handle_tool


tool_route = Blueprint("tool_bp", __name__, url_prefix="/tool")
tool_route.post("/result")(handle_tool)
