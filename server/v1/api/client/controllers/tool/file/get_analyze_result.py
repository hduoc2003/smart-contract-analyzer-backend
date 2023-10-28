from flask import request

from server.v1.api.client.models.file_collection import FileDoc
from server.v1.api.utils.StatusCode import StatusCode
from server.v1.api.utils.db_collection import get_document_by_id


def get_analyze_result():
    file_id = request.args.get('id')
    if file_id is None:
        return "No file_id provided"
    res: FileDoc | None = get_document_by_id(FileDoc, file_id) # type: ignore
    if res is not None:
        return res.to_json()
    else:
        return "File not found", StatusCode.NotFound.value  # Return a 404 Not Found status code
