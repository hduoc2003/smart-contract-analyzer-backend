from flask import jsonify
from mongoengine import Document, StringField, FloatField,ListField
import json
import os
import server.v1.config.app_config
from werkzeug.datastructures.file_storage import FileStorage

import uuid
from tools.types import FinalResult

class FileDoc(Document):
    submit_id = StringField()
    file_id = StringField(unique=True)  # Remove default value
    file_name = StringField(required=True)
    tool_name = StringField(required=True)
    duration = FloatField(required=True)
    solc= StringField(required=True)
    analysis = ListField(required=True)
    meta: dict[str, str] = {
        "collection": "files"
    }

def str_to_dict(data: str)->dict:
    return json.loads(data)

# def add_issue_ids(data) -> None:
#     for file in data:
#         count = 0
#         # Ensure there are issues in the JSON data
#         issues = file["analysis"]["issues"]
#         for issue in issues:
#             issue["id"] =  count # Generate a unique ObjectId and convert it to a string
#             count +=1


# def extract_file_res(result: dict) ->tuple[str, float, str, dict]:
#     file_name = result["file_name"]
#     duration = result["duration"]
#     tool_name = result["tool_name"]
#     analysis = result["analysis"]
#     return (file_name, tool_name,duration, analysis)

def save_file(id: str, file_id: str, file_data: FileStorage, user_name: str) -> None:
    try:
        user_storage: str = os.path.join(server.v1.config.app_config.get_local_storage_path(), user_name, id,"contracts")
        if not os.path.exists(user_storage):
            os.makedirs(user_storage)
        file_id = file_id +'.sol'
        file_data.save(os.path.join(user_storage, file_id))
    except Exception as e:
        print("File not exist")
def check_existed_id_in_volume(submit_id,user_name)-> bool:
    directory = os.path.join(server.v1.config.app_config.get_local_storage_path(), user_name)
    if submit_id in os.listdir(directory):
        return True
    return False
def get_file_by_id(id) -> FileDoc:
    file = FileDoc.objects(file_id=id).first()
    
    if file is not None:
        return file
    else:
        # If the specified ID is not found, you can raise an exception or return None
        # Here, we'll return None for simplicity
        return None # type: ignore
    
    
def get_submit_by_id(id) -> list[FileDoc]:
    submit = FileDoc.objects(submit_id=id)
    if submit:
        return submit
    else:
        return None # type: ignore


