from typing import Any
from flask import jsonify, request

from server.v1.api.client.models.file_collection import FileDoc
from server.v1.api.utils.FlaskLog import FlaskLog
from server.v1.api.utils.StatusCode import StatusCode
from server.v1.api.utils.db_collection import get_document


def get_analyze_result():
    file_id = request.args.get('id')
    if file_id is None:
        return "No file_id provided"
    res = FileDoc.minimize(file_id, json=True)
    if res is not None:
        return jsonify(res)
    else:
        return "File not found", StatusCode.NotFound.value  # Return a 404 Not Found status code
