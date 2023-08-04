import sys
import os
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask
from server.route.login.login import login_route
from server.route.signup.signup import signup_route
from server.route.tool.tool import tool_route

load_dotenv()
PORT = int(os.getenv("PORT") or 5000)

app = Flask(__name__)
app.register_blueprint(login_route)
app.register_blueprint(signup_route)
app.register_blueprint(tool_route)

@app.route("/")
def response():
    return "hello"

if __name__ == "__main__":
    app.run(debug=True, port=PORT)
