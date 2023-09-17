from flask import Blueprint, session, jsonify
from server.v1.api.client.controllers.tool_controller import handle_files, handle_result_id


tool_route = Blueprint("tool_bp", __name__, url_prefix="/tool")
tool_route.post("/handle_files")(handle_files)
tool_route.post("/handle_results")(handle_result_id)
# Print out all session values
@tool_route.route('/print_session')
def print_session():
    session_values = {key: session[key] for key in session}
    return jsonify(session_values)