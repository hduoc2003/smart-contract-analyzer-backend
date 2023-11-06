from server.v1.api.client.controllers.tool.file.get_analyze_result import get_analyze_result
from server.v1.api.client.controllers.tool.submit.get_analyze_status import get_analyze_status
from server.v1.api.client.controllers.tool.submit.handle_resubmit import handle_resubmit
from server.v1.api.client.controllers.tool.submit.handle_submit import handle_submit
from server.v1.api.client.controllers.tool.submit.socket.listen_analyze_status_change import (
    listen_analyze_status_change
)


class ToolController:
    handle_submit = handle_submit
    get_analyze_status = get_analyze_status
    get_analyze_result = get_analyze_result
    listen_analyze_status_change = listen_analyze_status_change
    handle_resubmit= handle_resubmit
