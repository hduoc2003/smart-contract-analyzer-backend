from server.v1.api.client.controllers.auth.signin_controller import handle_signin
from server.v1.api.client.controllers.auth.signup_controller import handle_signup

class AuthController:
    handle_signin = handle_signin
    handle_signup = handle_signup
