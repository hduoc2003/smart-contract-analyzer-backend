# database/db_connection.py
from mongoengine import connect
from dotenv import load_dotenv
import os

load_dotenv()
CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
DATABASE_NAME = "Tool-Integrating"

def connect_to_database():
    connect(
        DATABASE_NAME,
        host=CONNECTION_STRING,  # Use the MongoDB Atlas connection string here
    )