from flask import Blueprint

from server.v1.api.client.controllers.tool.ToolController import ToolController

file_route = Blueprint("file_bp", __name__, url_prefix="/file")

file_route.get('/get-analyze-result')(ToolController.get_analyze_result)
