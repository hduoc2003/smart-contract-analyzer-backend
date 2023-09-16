import os
from mongoengine import connect
from server.v1.api.utils.server_env import get_env

CONNECTION_STRING: str = get_env("MONGO_CONNECTION_STRING")
DATABASE_NAME: str = get_env("DATABASE_NAME")

def init_database() -> None:
    connect(
        DATABASE_NAME,
        host=CONNECTION_STRING,
    )
