from flask import Blueprint


tool_route = Blueprint("tool", __name__, url_prefix="/tool")

@tool_route.route("/")
def response():
    return {

    }
