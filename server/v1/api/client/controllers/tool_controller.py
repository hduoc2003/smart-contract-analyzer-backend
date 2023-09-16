from typing import Generator
from flask import Response, jsonify, request
from tools.Tool import Tool
from server.v1.api.utils.StatusCode import StatusCode
from server.v1.api.utils.FlaskLog import *
from server.v1.api.client.models.tools_collection import *
import threading
from werkzeug.datastructures.file_storage import FileStorage
from werkzeug.datastructures.structures import ImmutableMultiDict
from _collections_abc import dict_keys
from tools.types import ToolAnalyzeArgs
from tools.utils.parsers import obj_to_jsonstr

def create_file_doc_background(result) -> None:
    # Run create_file_doc asynchronously in a background thread
    thread = threading.Thread(target=create_file_doc, args=(result,))
    thread.start()

def handle_tool():
    user_name = "phu21122003"
    tools: list[str] = ["Mythril", "Slither"]
    if request is None:
        return jsonify({"message": "Nothing requested"}), StatusCode.BadRequest.value

    files_data: ImmutableMultiDict[str, FileStorage] = request.files
    file_keys: dict_keys[str, FileStorage] = files_data.keys()
    file_list:list[str] = []

    for file_key in file_keys:
        file_data: FileStorage = files_data[file_key]
        file_name: str | None = file_data.filename
        if (file_name is None):
            continue
        save_file(file_name, file_data, user_name)

        file_list.append(file_name)

    FlaskLog.info(f"{file_list} {tools}  {user_name}")
    result_stream: Generator = Tool.analyze_files_async(
        files=[
            ToolAnalyzeArgs(
                sub_container_file_path=f"{user_name}/contracts",
                file_name=file_name,
            ) for file_name in file_list
        ],
        stream=True
    ) # type: ignore
    def temp() -> Generator[str, Any, None]:
        for i in result_stream:
            yield obj_to_jsonstr(i)
    return Response(temp())
    # add_issue_ids(result)
    # create_file_doc_background(result)

# def test_streaming():
#     stream: Generator | list = Tool.analyze_files_async(
#         files=[
#             ToolAnalyzeArgs(
#                 sub_container_file_path="user1/contracts",
#                 file_name="swc-127.sol"
#             )
#             ,ToolAnalyzeArgs(
#                 sub_container_file_path="user1/contracts",
#                 file_name="swc-106.sol"
#             )
#         ],
#         stream=True
#     )

#     def temp():
#         for i in stream:
#             yield obj_to_jsonstr(i)
#     return Response(temp())


