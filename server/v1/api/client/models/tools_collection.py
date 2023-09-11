from enum import Enum
from mongoengine import Document, StringField, FloatField,BooleanField, DateTimeField, EnumField, IntField, FileField, ListField, EmbeddedDocumentField, EmbeddedDocument, DictField
from datetime import datetime
from bson import ObjectId  # Import ObjectId for generating unique IDs
import json
from server.v1.api.utils.FlaskLog import FlaskLog
import os
import server.v1.config.app_config

import uuid

class FileDoc(Document):
    file_id = StringField(unique=True)  # Remove default value
    file_name = StringField(required=True)
    tool_name = StringField(required=True)
    duration = FloatField(required=True)
    analysis = ListField(required=True)
    meta = {
        "collection": "files"
    }
    
def str_to_dict(data: str)->dict:
    return json.loads(data)
def add_issue_ids(data: dict) ->dict:
    for file in data:
        count = 0
        # Ensure there are issues in the JSON data
        issues = file["analysis"]["issues"]    
        for issue in issues:
            issue["id"] =  count # Generate a unique ObjectId and convert it to a string
            count +=1

def create_file_doc(result: dict):
    for file in result:
        (file_name, tool_name, duration, analysis) = extract_file_res(file)
        issues = []
        count = 0
        for issue_data in analysis["issues"]:
            issue = {
                "id": count,
                "contract": issue_data["contract"],
                "source_map": issue_data["source_map"],
                "line_no": issue_data["line_no"],
                "code": issue_data["code"],
                "description": issue_data["description"],
                "hint": issue_data["hint"],
                "issue_title": issue_data["issue_title"],
                "swcID": issue_data["swcID"],
                "swc_title": issue_data["swc_title"],
                "swc_link": issue_data["swc_link"],
                "severity": issue_data["severity"]
            }
            count += 1
            issues.append(issue)
        new_file = FileDoc(
            file_id = str(uuid.uuid4()),
            file_name=file_name,
            tool_name=tool_name,
            duration=duration,
            analysis=[
                {
                    "errors": "null"
                },
                {
                    "issues": issues
                }
            ]
        )
        new_file.save()

def extract_file_res(result: dict) ->(str, float, str, dict):
    file_name = result["file_name"]
    duration = result["duration"]
    tool_name = result["tool_name"]
    analysis = result["analysis"]
    return (file_name, tool_name,duration, analysis)

def save_file_to_local_storage(file_name, file_content, user_name):
    user_storage = os.path.join(server.v1.config.app_config.get_local_storage_path(), user_name, "contracts")
    if not os.path.exists(user_storage):
        os.makedirs(user_storage)
    
    file_path = os.path.join(user_storage, file_name)
    
    try:
        with open(file_path, 'wb') as file:
            file.write(file_content)
    except Exception as e:
        FlaskLog.err(f"Cannot write into contract file: {e}")
