from flask import Blueprint

from server.v1.api.utils.FlaskLog import FlaskLog

test_route = Blueprint("test_bp", __name__, url_prefix="/haha")

def test():
    print('test')
    return 'test'

test_route.route("", methods=["GET"])(test)
