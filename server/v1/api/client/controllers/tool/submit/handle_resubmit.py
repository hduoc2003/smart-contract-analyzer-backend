
from dataclasses import dataclass

from flask import jsonify, request
from server.v1.api.client.controllers.tool.submit.handle_submit import start_analyzing
from server.v1.api.client.models.file_collection import FileDoc

from server.v1.api.utils.StatusCode import StatusCode
from server.v1.api.utils.db_collection import get_document_includes
from server.v1.api.utils.gen_id import gen_id

@dataclass
class ReSubmitRequest:
    old_file_id: str
    new_file_name: str
    source_code: str
    user_id: str

def handle_resubmit():
    if (request.json is None):
        return jsonify({'msg': 'No data provided'}), StatusCode.BadRequest.value
    resubmit_data = ReSubmitRequest(**request.json)
    file_info: FileDoc | None = get_document_includes(FileDoc, id=resubmit_data.old_file_id, included_fields=['submit_id']) # type: ignore
    if (file_info is None):
        return jsonify({'msg': 'Wrong submit id'}), StatusCode.BadRequest.value
    submit_id: str = str(file_info.submit_id)
    new_file_id = gen_id()

    start_analyzing(
        submit_id=submit_id,
        user_id=resubmit_data.user_id,
        files_ids=[new_file_id],
        files_name=[resubmit_data.new_file_name],
        files_sourcode=[resubmit_data.source_code]
    )

    return jsonify({
        'submit_id': file_info.submit_id
    })
