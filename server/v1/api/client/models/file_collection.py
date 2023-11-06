import datetime
from enum import Enum
from typing import Any, Union
from mongoengine import Document, StringField, FloatField, EnumField, DictField, DateTimeField, DateField
from server.v1.api.utils.db_collection import get_document_excludes
from server.v1.config.database_config import db

file_collection = db.files
class AnalyzeStatus(Enum):
    ANALYZING = "Analyzing"
    ERROR = "Error"
    COMPLETED = "Completed"
class FileDoc(Document):
    id = StringField(primary_key=True)  # Remove default value
    file_name = StringField(required=True)
    status=EnumField(AnalyzeStatus, required=True)
    tool_name = StringField(required=True, default="")
    duration = FloatField(required=True, default=0)
    solc= StringField(required=True, default="")
    analysis = DictField(required=True, default={"error": [], "issues": []})
    source_code = StringField(required=True)
    submit_id = StringField(required=True)
    created_at = DateTimeField(required=True, default=datetime.datetime.now())
    meta: dict[str, str] = {
        "collection": "files"
    }

    # def minimize_self(
    #     self,
    #     excluded_fields:list[str]=['tool_name', 'created_at'],
    #     json: bool = False,
    #     json_str: bool = False
    # ) -> Union["FileDoc", str, dict[str, Any]]:
    #     if (not json) and (not json_str):
    #         return FileDoc(

    #         )

    @staticmethod
    def minimize(
        id:str,
        excluded_fields:list[str]=['tool_name'],
        json: bool = False
    ) -> Union["FileDoc", dict[str, Any], None]:
        return get_document_excludes(FileDoc, id, excluded_fields, json=json)



