from flask import jsonify
from mongoengine import Document, StringField, FloatField,ListField
import json
import os
import server.v1.config.app_config
from werkzeug.datastructures.file_storage import FileStorage

import uuid
from tools.types import FinalResult

class FileDoc(Document):
    file_id = StringField(unique=True)  # Remove default value
    file_name = StringField(required=True)
    tool_name = StringField(required=True)
    duration = FloatField(required=True)
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

def create_file_doc(result: FinalResult) -> list[str]:
    # (file_name, tool_name, duration, analysis) = extract_file_res(result)
    file_name = result.file_name
    tool_name = result.tool_name
    duration = result.duration
    analysis = result.analysis
    issues = []
    count = 0
    files_id: list[str] = [] 
    for issue_data in analysis.issues:
        issue = {
            "id": count,
            "contract": issue_data.contract,
            "source_map": issue_data.source_map,
            "line_no": issue_data.line_no,
            "code": issue_data.code,
            "description": issue_data.description,
            "hint": issue_data.hint,
            "issue_title": issue_data.issue_title,
            "swcID": issue_data.swcID,
            "swc_title": issue_data.swc_title,
            "swc_link": issue_data.swc_link,
            "severity": issue_data.severity
        }
        count += 1
        issues.append(issue)
    file_id = str(uuid.uuid4())
    new_file = FileDoc(
        file_id=file_id,
        file_name=file_name,
        tool_name=tool_name,
        duration=duration,
        analysis=[
            {
                "errors": analysis.errors
            },
            {
                "issues": issues
            }
        ]
    )
    new_file.save()
    return files_id

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
        
def get_file_by_id(id) -> FileDoc:
    file = FileDoc.objects(file_id = id).first()
    return file