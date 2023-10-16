from mongoengine import Document, StringField, DateTimeField, ListField
from datetime import datetime

from server.v1.api.client.models.file_collection import FileDoc
from server.v1.api.utils.FlaskLog import FlaskLog

class SubmitDoc(Document):
    id = StringField(primary_key=True)
    files_ids = ListField(StringField(), required=True)
    createdAt = DateTimeField(default=datetime.utcnow())

    meta: dict[str, str] = {
        'collection': 'submits'
    }

    @classmethod
    def get_all_files(cls, submit_id: str) -> list[FileDoc]:
        submit: SubmitDoc = cls.objects(id=submit_id).first()
        if submit is None:
            return []
        files_ids: list[str] = submit.files_ids # type: ignore
        return [FileDoc.objects(id=file_id).first() for file_id in files_ids]

