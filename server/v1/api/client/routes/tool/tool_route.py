import uuid
from flask import Blueprint, Response, request, session, jsonify
from flask_cors import cross_origin
from server.v1.api.client.models.submit_collection import SubmitDoc
from server.v1.api.utils.Async import Async
from server.v1.api.utils.parsers import obj_to_json
from tools.Tool import Tool
from server.v1.api.utils.StatusCode import StatusCode
from server.v1.api.utils.FlaskLog import *
from server.v1.api.client.models.file_collection import *
from werkzeug.datastructures.file_storage import FileStorage
from werkzeug.datastructures.structures import ImmutableMultiDict
from _collections_abc import dict_keys
from tools.types import AnalysisResult, ToolAnalyzeArgs
from tools.types import FinalResult
from typing import Generator
from server.v1.api.utils.StatusCode import StatusCode
from server.v1.api.utils.DBCollection import update_one

tool_route = Blueprint("tool_bp", __name__, url_prefix="/tool")

map_id_to_name: dict[str, str] = {

}

@tool_route.route("/handle_files",methods=["POST"])
@cross_origin(supports_credentials=True)
def handle_files():
    user_name = "tung123"
    submit_id = str(generate_request_id())

    if request is None:
        return jsonify({"message": "Nothing requested"}), StatusCode.BadRequest.value

    files_data: ImmutableMultiDict[str, FileStorage] = request.files
    file_keys: dict_keys[str, FileStorage] = files_data.keys()

    response_data: dict[str, str] = {'uuid': submit_id}
    files_ids: list[str] = []

    for file_key in file_keys:
        file_data: FileStorage = files_data[file_key]
        file_id: str = str(generate_request_id())
        file_name: str | None = file_data.filename
        if (file_name is None):
            continue
        source_code = save_file(submit_id, file_id, file_data, user_name)
        response_data[file_name] = file_id
        files_ids.append(file_id)
        map_id_to_name[file_id + ".sol"] = file_name
        FileDoc(
            id=file_id,
            file_name=file_name,
            status=AnalyzeStatus.ANALYZING,
            source_code=source_code
        ).save()
        # FlaskLog.info(file_data.stream.read())

    SubmitDoc(
        id=submit_id,
        files_ids=files_ids
    ).save()

    def start_analyzing():
        result_stream: Generator = Tool.analyze_files_async(
            files=[
                ToolAnalyzeArgs(
                    sub_container_file_path=f"{user_name}/{submit_id}/contracts/",
                    file_name=f"{file_id}.sol",
                ) for file_id in files_ids
            ],
            stream=True
        ) # type: ignore
        for final_result in result_stream:
            final_result: FinalResult
            update_result(final_result, True)

    Async.run_functions([start_analyzing], [[]], detach=True)

    session["id"] = submit_id

    # print("SESSION ID", session.get('id'))

    return jsonify(response_data)

count_enter = {}
@tool_route.route("/handle_results",methods=["GET"])
@cross_origin(supports_credentials=True)
def handle_result_id():
    submit_id: str | None = request.args.get('id')
    if submit_id is None:
        return "No submit_id provided"

    def temp():
        files_results: list[FileDoc] = SubmitDoc.get_all_files(submit_id)
        cnt_done: int = 0
        analyzing_files: list[StringField] = []
        for file_result in files_results:
            if (file_result.status != AnalyzeStatus.ANALYZING):
                cnt_done += 1
                yield(file_result.to_json())
            else:
                analyzing_files.append(file_result.id)

        if (cnt_done == len(files_results)):
            return

        pipeline = [
            {
                "$match": {
                    "updateDescription.updatedFields.status": {"$exists": True},
                    "documentKey._id": {"$in": analyzing_files}
                }
            }
        ]
        # FlaskLog.info(cnt_done)
        change_stream = file_collection.watch(pipeline=pipeline, full_document="updateLookup")
        for change in change_stream:
            cnt_done += 1
            yield(json.dumps(change.get('fullDocument')))
            if (cnt_done == len(files_results)):
                change_stream.close()
                break

    return Response(temp())

# Print out all session values
@tool_route.route('/print_session',methods=["GET"])
@cross_origin(supports_credentials=True)
def print_session():
    session_values = {key: session[key] for key in session}
    return jsonify(session_values)

def generate_request_id():
    new_id = uuid.uuid4()
    return new_id

@tool_route.route('/handle_file_id', methods=["GET"])
@cross_origin(supports_credentials=True)
def handle_file_id():
    id_param = request.args.get('id')
    if id_param is None:
        return "No file_id provided"
    file: FileDoc = get_file_by_id(id_param)

    if file is not None:
        return file.to_json()
    else:
        return "File not found", StatusCode.NotFound.value  # Return a 404 Not Found status code

def update_result(result: FinalResult, detach: bool = False):
    def main():
        tool_name: str = result.tool_name
        duration: float = result.duration
        solc: str = result.solc
        analysis: AnalysisResult = result.analysis
        issues = []
        count = 0
        for issue_data in analysis.issues:
            issue = {
                "id": count,
                "contract": issue_data.contract,
                "source_map": issue_data.source_map,
                "line_no": issue_data.line_no,
                "code": issue_data.code,
                "description": issue_data.description,
                "hint": issue_data.hint,
                "issue_title": issue_data.issue_title,
                "swcID": issue_data.swcID,
                "swc_title": issue_data.swc_title,
                "swc_link": issue_data.swc_link,
                "severity": issue_data.severity
            }
            count += 1
            issues.append(issue)

        file_id: str = result.file_name.replace(".sol", "")
        status: AnalyzeStatus = AnalyzeStatus.ERROR if len(analysis.errors) != 0 else AnalyzeStatus.DONE

        try:
            update_one(doc=FileDoc, data={
                "status": status,
                "tool_name": tool_name,
                "duration": duration,
                "solc": solc,
                "analysis": [{
                        "errors": obj_to_json(analysis.errors)
                    }, {
                        "issues": issues
                    }
                ]
            }, id=file_id)

        except Exception as exc:
            # for field in vars(FileDoc):    # You could also loop in User._fields to make something generic
            #     if field in str(exc):
            FlaskLog.err(exc)
            # FlaskLog.err('field {} is not unique'.format(field))
            # FlaskLog.err(new_file.id)

        del map_id_to_name[result.file_name]

    if detach:
        Async.run_functions([main], [[]], True)
    else:
        main()
    # return files_id
