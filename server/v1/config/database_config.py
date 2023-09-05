import os
from mongoengine import connect
from server.v1.api.utils.server_env import get_env

CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
DATABASE_NAME = os.getenv("DATABASE_NAME")

def init_database():
    connect(
        DATABASE_NAME,
        host=CONNECTION_STRING,
    )
