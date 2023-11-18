from flask_socketio import SocketIO
from typing import Any
from server.v1.api.client.controllers.tool.ToolController import ToolController

def init_socket_events(socketio: SocketIO) -> None:

    @socketio.on('listen-analyze-status-change')
    def listen_analyze_status_change(data: Any) -> None:
        ToolController.listen_analyze_status_change(data)
