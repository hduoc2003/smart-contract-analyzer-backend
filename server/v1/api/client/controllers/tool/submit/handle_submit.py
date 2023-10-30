
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
from server.v1.api.utils.db_collection import get_document, update_one

from server.v1.api.utils.gen_id import gen_id
from server.v1.api.utils.parsers import obj_to_json, obj_to_jsonstr
from server.v1.api.utils.path import get_subcontainer_file_path
from server.v1.api.utils.save_contract import save_contract
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
    user_id = "tung123"
    submit_id = gen_id()

    files_data: ImmutableMultiDict[str, FileStorage] = request.files
    file_keys: dict_keys[str, FileStorage] = files_data.keys()

    response_data: SubmitResponse = SubmitResponse(submit_id=submit_id, files_info=[])
    files_sourcode: list[FileStorage] = []

    for file_key in file_keys:
        file_data: FileStorage = files_data[file_key]
        file_id: str = str(gen_id())
        file_name: str | None = file_data.filename
        if (file_name is None):
            continue
        response_data.files_info.append(FileInfo(
            file_id=file_id,
            file_name=file_name
        ))
        files_sourcode.append(file_data)
        # FlaskLog.info(file_data.stream.read())
    if len(files_sourcode) == 0:
        return 'No file provided', StatusCode.BadRequest.value

    start_analyzing(
        submit_id=submit_id,
        user_id=user_id,
        files_ids=[file_info.file_id for file_info in response_data.files_info],
        files_name=[file_info.file_name for file_info in response_data.files_info],
        files_sourcode=files_sourcode
    )

    return jsonify(obj_to_jsonstr(response_data))

def start_analyzing(
    submit_id: str,
    user_id,
    files_ids: list[str],
    files_name: list[str],
    files_sourcode: list[FileStorage] | list[str],
    detach: bool = True
) -> None:
    for i, file_id in enumerate(files_ids):
        source_code: str = save_contract(
            submit_id=submit_id,
            file_id=file_id,
            file_data=files_sourcode[i],
            user_id=user_id
        )
        FileDoc(
            id=file_id,
            file_name=files_name[i],
            status=AnalyzeStatus.ANALYZING,
            source_code=source_code,
            submit_id=submit_id
        ).save()
    submit_doc: SubmitDoc | None = get_document(SubmitDoc, submit_id)
    if submit_doc is None:
        SubmitDoc(id=submit_id,files_ids=files_ids).save()
    else:
        submit_doc.update(push_all__files_ids=files_ids)

    def analyze():
        result_stream: Generator = Tool.analyze_files_async(
            files=[
                ToolAnalyzeArgs(
                    sub_container_file_path=get_subcontainer_file_path(user_id, submit_id),
                    file_name=f"{file_id}.sol",
                ) for file_id in files_ids
            ],
            stream=True
        ) # type: ignore
        for final_result in result_stream:
            final_result: FinalResult
            update_result(final_result, True)

    Async.run_functions([analyze], [[]], detach=detach)

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
