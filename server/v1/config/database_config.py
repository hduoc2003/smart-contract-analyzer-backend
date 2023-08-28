from server.v1.api.utils.FlaskLog import FlaskLog
from server.v1.api.utils.server_env import get_env
from mongoengine import connect

def init_database() -> None:
    CONNECTION_STRING: str = get_env("MONGO_CONNECTION_STRING")
    DATABASE_NAME: str = get_env("DATABASE_NAME")

    connect(
        db=DATABASE_NAME,
        host=CONNECTION_STRING
    )
