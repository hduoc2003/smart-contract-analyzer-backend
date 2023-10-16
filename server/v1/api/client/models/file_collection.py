from enum import Enum
from mongoengine import Document, StringField, FloatField, ListField, EnumField
import json
import os
from server.v1.api.utils.path import get_contracts_storage_path
from werkzeug.datastructures.file_storage import FileStorage
from server.v1.config.database_config import db

file_collection = db.files

class AnalyzeStatus(Enum):
    ANALYZING = "Analyzing"
    ERROR = "Error"
    DONE = "Done"

class FileDoc(Document):
    id = StringField(primary_key=True)  # Remove default value
    file_name = StringField(required=True)
    status=EnumField(AnalyzeStatus, required=True)
    tool_name = StringField(required=True, default="")
    duration = FloatField(required=True, default=0)
    solc= StringField(required=True, default="")
    analysis = ListField(required=True, default=["N/A"])
    source_code = StringField(required=True)

    meta: dict[str, str] = {
        "collection": "files"
    }

def str_to_dict(data: str)->dict:
    return json.loads(data)

def save_file(id: str, file_id: str, file_data: FileStorage, user_name: str) -> str:
    try:
        user_storage: str = get_contracts_storage_path(username=user_name, submit_id=id)
        if not os.path.exists(user_storage):
            os.makedirs(user_storage)
        path: str = os.path.join(user_storage, file_id +'.sol')
        file_data.save(path)
        with open(path, "r") as source_code:
            return source_code.read()
    except Exception as e:
        print("File not exist")
        return ""

def get_file_by_id(id: str) -> FileDoc:
    file = FileDoc.objects(id=id).first()

    if file is not None:
        return file
    else:
        # If the specified ID is not found, you can raise an exception or return None
        # Here, we'll return None for simplicity
        return None # type: ignore


