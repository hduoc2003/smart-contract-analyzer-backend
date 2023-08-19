from flask import Blueprint


login_route = Blueprint("login", __name__, url_prefix="/login")

@login_route.route("/")
def response():
    return {

    }
