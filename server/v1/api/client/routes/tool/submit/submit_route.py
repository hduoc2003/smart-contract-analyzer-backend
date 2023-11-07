from flask import Blueprint

from server.v1.api.client.controllers.tool.ToolController import ToolController

submit_route = Blueprint("submit_bp", __name__, url_prefix="/submit")
submit_route.post('')(ToolController.handle_submit)
submit_route.get('/get-analyze-status')(ToolController.get_analyze_status)
submit_route.post('/resubmit')(ToolController.handle_resubmit)

