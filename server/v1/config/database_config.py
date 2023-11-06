from mongoengine import connect
from pymongo import MongoClient
from server.v1.api.utils.server_env import get_env

CONNECTION_STRING: str = get_env("MONGO_CONNECTION_STRING")
DATABASE_NAME: str = get_env("DATABASE_NAME")

client: MongoClient
db = None

def init_database() -> None:
    connect(
        DATABASE_NAME,
        host=CONNECTION_STRING,
    )

    global client
    global db

    client = MongoClient(CONNECTION_STRING)
    db = client[DATABASE_NAME]


