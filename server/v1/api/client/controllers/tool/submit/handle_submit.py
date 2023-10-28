
from dataclasses import dataclass
from typing import Generator
from flask import jsonify, request
from server.v1.api.client.models.file_collection import AnalyzeStatus, FileDoc
from server.v1.api.client.models.submit_collection import SubmitDoc
from server.v1.api.utils.Async import Async
from server.v1.api.utils.FlaskLog import FlaskLog
from server.v1.api.utils.StatusCode import StatusCode
from werkzeug.datastructures.file_storage import FileStorage
from werkzeug.datastructures.structures import ImmutableMultiDict
from _collections_abc import dict_keys
from server.v1.api.utils.db_collection import update_one

from server.v1.api.utils.gen_id import gen_id
from server.v1.api.utils.parsers import obj_to_json, obj_to_jsonstr
from server.v1.api.utils.save_contract import save_file
from tools.Tool import Tool
from tools.types import AnalysisResult, FinalResult, ToolAnalyzeArgs

@dataclass
class FileInfo:
    file_id: str
    file_name: str

@dataclass
class SubmitResponse:
    submit_id: str
    files_info: list[FileInfo]

def handle_submit():
    """
        response type {
            'submit_id': str (id of this submit)
            '
        }

    Returns:
        _type_: _description_
    """
    user_name = "tung123"
    submit_id = gen_id()

    if request is None:
        return jsonify({"message": "Nothing requested"}), StatusCode.BadRequest.value

    files_data: ImmutableMultiDict[str, FileStorage] = request.files
    file_keys: dict_keys[str, FileStorage] = files_data.keys()

    response_data: SubmitResponse = SubmitResponse(submit_id=submit_id, files_info=[])
    files_ids: list[str] = []

    for file_key in file_keys:
        file_data: FileStorage = files_data[file_key]
        file_id: str = str(gen_id())
        file_name: str | None = file_data.filename
        if (file_name is None):
            continue
        source_code = save_file(submit_id, file_id, file_data, user_name)
        response_data.files_info.append(FileInfo(
            file_id=file_id,
            file_name=file_name
        ))
        files_ids.append(file_id)
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

    return jsonify(obj_to_jsonstr(response_data))

def update_result(result: FinalResult, detach: bool = False):
    def main():
        tool_name: str = result.tool_name
        duration: float = result.duration
        solc: str = result.solc
        analysis: AnalysisResult = result.analysis

        file_id: str = result.file_name.replace(".sol", "")
        status: AnalyzeStatus = AnalyzeStatus.ERROR if len(analysis.errors) != 0 else AnalyzeStatus.COMPLETED

        try:
            update_one(doc=FileDoc, data={
                "status": status,
                "tool_name": tool_name,
                "duration": duration,
                "solc": solc,
                "analysis": obj_to_json(analysis)

            }, id=file_id)

        except Exception as exc:
            # for field in vars(FileDoc):    # You could also loop in User._fields to make something generic
            #     if field in str(exc):
            FlaskLog.err(exc)
            # FlaskLog.err('field {} is not unique'.format(field))
            # FlaskLog.err(new_file.id)

    if detach:
        Async.run_functions([main], [[]], True)
    else:
        main()
