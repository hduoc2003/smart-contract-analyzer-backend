from flask_cors import CORS, cross_origin

def setup_app_config(app):
    CORS(app, resources={r"/*": {"origins": "*"}},  supports_credentials=True)
