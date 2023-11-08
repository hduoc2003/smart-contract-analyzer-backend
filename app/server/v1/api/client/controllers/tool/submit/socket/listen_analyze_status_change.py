from typing import Any
from dataclasses import dataclass

from flask_socketio import emit
from server.v1.api.client.controllers.tool.submit.get_analyze_status import create_response
from server.v1.api.client.models.file_collection import file_collection
from server.v1.api.utils.FlaskLog import FlaskLog

@dataclass
class Data:
    analyzing_files_id: list[str]
    cnt_analyzing: int

def listen_analyze_status_change(data: Any) -> None:
    casted_data: Data = Data(**data)
    print(data)
    FlaskLog.info(casted_data)
    if (casted_data.cnt_analyzing == 0):
        emit('close-listen-analyze-status-change')
        return

    pipeline = [
        {
            "$match": {
                "updateDescription.updatedFields.status": {"$exists": True},
                "documentKey._id": {"$in": casted_data.analyzing_files_id}
            }
        }
    ]
    # FlaskLog.info(cnt_done)
    change_stream = file_collection.watch(pipeline=pipeline, full_document="updateLookup")
    for change in change_stream:
        casted_data.cnt_analyzing -= 1
        file_result: dict[str, Any] = change.get('fullDocument')
        emit('send-analyze-status-change', create_response(
            file_id=file_result['_id'],
            file_name=file_result['file_name'],
            status=file_result['status']
        ))
        if (casted_data.cnt_analyzing == 0):
            change_stream.close()
            emit('close-listen-analyze-status-change')
            break
