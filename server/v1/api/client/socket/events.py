from typing import Any
from server.v1.api.client.controllers.tool.ToolController import ToolController
from server.v1.config.app_config import socketio

@socketio.on('listen-analyze-status-change')
def listen_analyze_status_change(data: Any) -> None:
    ToolController.listen_analyze_status_change(data)
