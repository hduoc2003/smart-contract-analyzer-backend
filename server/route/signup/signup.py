from flask import Blueprint


signup_route = Blueprint("signup", __name__, url_prefix="/signup")

@signup_route.route("/")
def response():
    return {

    }
