from enum import Enum
from typing import Any
from mongoengine import Document, StringField, FloatField, EnumField, DictField
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

    meta: dict[str, str] = {
        "collection": "files"
    }

    def get_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "file_name": self.file_name,
            "status": self.status,
            "tool_name": self.tool_name,
            "duration": self.duration,
            "solc": self.solc,
            "analysis": self.analysis,
            "source_code": self.source_code,
        }


