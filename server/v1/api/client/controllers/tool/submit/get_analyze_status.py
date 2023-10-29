from flask import jsonify, request

from server.v1.api.client.models.file_collection import AnalyzeStatus, FileDoc
from server.v1.api.client.models.submit_collection import SubmitDoc


__all__ = ['get_analyze_status']

def create_response(file_id: str, file_name: str, status: AnalyzeStatus | str) -> dict[str, str]:
    return {
        'file_id': file_id,
        'file_name': file_name,
        'status': status if isinstance(status, str) else status.value
    }

def get_analyze_status():
    """ response type [{
        'file_id': str (id of this file),
        'file_name': str (name of this file),
        'status': AnalyzeStatus (status of this file)

    }]: list of file of this submit

    Returns:
        _type_: _description_
    """
    submit_id: str | None = request.args.get('id')
    if submit_id is None:
        return "No submit_id provided"

    filesInfo: list[FileDoc] = SubmitDoc.get_all_files(
        submit_id=submit_id,
        needed_field=['id', 'file_name', 'status']
    )

    return jsonify(
        [create_response(
            file_id=fileInfo.id, # type: ignore
            file_name=fileInfo.file_name, # type: ignore
            status=fileInfo.status # type: ignore
        ) for fileInfo in filesInfo]
    )

    # pipeline = [
    #     {
    #         "$match": {
    #             "updateDescription.updatedFields.status": {"$exists": True},
    #             "documentKey._id": {"$in": analyzing_files}
    #         }
    #     }
    # ]
    # # FlaskLog.info(cnt_done)
    # change_stream = file_collection.watch(pipeline=pipeline, full_document="updateLookup")
    # for change in change_stream:
    #     cnt_done += 1
    #     file_result = change.get('fullDocument')
    #     if (cnt_done == len(files_results)):
    #         change_stream.close()
    #         break

    # return Response(temp())
