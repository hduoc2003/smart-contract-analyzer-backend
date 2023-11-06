from typing import Any
from mongoengine import Document, StringField, DateTimeField, ListField
from datetime import datetime

from server.v1.api.client.models.file_collection import FileDoc
from server.v1.api.utils.FlaskLog import FlaskLog
from server.v1.api.utils.db_collection import get_document, get_document_includes

class SubmitDoc(Document):
    id = StringField(primary_key=True)
    files_ids = ListField(StringField(), required=True)
    createdAt = DateTimeField(default=datetime.utcnow())

    meta: dict[str, str] = {
        'collection': 'submits'
    }

    @classmethod
    def get_all_files(cls, submit_id: str, needed_field: str | list[str] = '_all') -> list[FileDoc] | None:
        submit: SubmitDoc | None | dict[str, Any] = get_document_includes(SubmitDoc, submit_id, ['files_ids'])
        if submit is None:
            return None
        files_ids: list[str] = submit.files_ids # type: ignore
        res: list[FileDoc] = []
        for file_id in files_ids:
            element: FileDoc | None = get_document(FileDoc, file_id)
            if (element is None):
                raise Exception(f'file_id {file_id} is missing from submit {submit_id}')
            res.append(element)

        if (isinstance(needed_field, list)):
            res: list[FileDoc] = []
            for file_id in files_ids:
                file = get_document_includes(FileDoc, file_id, needed_field)
                if isinstance(file, FileDoc):
                    res.append(file)
            return res
        return []
