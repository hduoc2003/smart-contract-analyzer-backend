# from typing import Generator
# from flask import Response, jsonify, request ,session
# from tools.Tool import Tool
# from server.v1.api.utils.StatusCode import StatusCode
# from server.v1.api.utils.FlaskLog import *
# from server.v1.api.client.models.tools_collection import *
# import threading
# from werkzeug.datastructures.file_storage import FileStorage
# from werkzeug.datastructures.structures import ImmutableMultiDict
# from _collections_abc import dict_keys
# from tools.types import ToolAnalyzeArgs
# from tools.utils.parsers import obj_to_jsonstr, obj_to_json
# from tools.types import FinalResult
# import flask


# def create_file_doc_background(result:FinalResult) -> None:
#     # Run create_file_doc asynchronously in a background thread
#     thread = threading.Thread(target=create_file_doc, args=(result,))
#     thread.start()

# def handle_result_id():
#     user_name = "tung123"

#     id_param = request.args.get('id')
#     print(id_param)
#     print(session.values)
#     if not id_param:
#         return "The 'id' query parameter is missing."
#     if id_param != session["id"]:
#         return "Nope wrong id matching", 400

#     files_list = session["files_list"]
#     result_stream: Generator = Tool.analyze_files_async(
#         files=[
#             ToolAnalyzeArgs(
#                 sub_container_file_path=f"{user_name}/{id_param}/contracts/",
#                 file_name=file_name,
#             ) for file_name in files_list
#         ],
#         stream=True
#     ) # type: ignore
#     def temp() -> Generator[str, Any, None]:
#         for final_result in result_stream:
#             # final_result: FinalResult
#             create_file_doc_background(final_result)
            
#             yield obj_to_jsonstr(final_result)
#     session.pop('id', None)
#     session.pop('files_list', None)
#     return Response(temp())

# def handle_files():
#     user_name = "tung123"
#     #TODO:gen_id
#     id = generate_request_id()
#     id_str = str(id)
    
    
#     #store file to local storage
   
#     if request is None:
#         return jsonify({"message": "Nothing requested"}), StatusCode.BadRequest.value
#     files_data: ImmutableMultiDict[str, FileStorage] = request.files
#     file_keys: dict_keys[str, FileStorage] = files_data.keys()
#     files_list:list[str] = []

#     for file_key in file_keys:
#         file_data: FileStorage = files_data[file_key]
#         file_name: str | None = file_data.filename
#         if (file_name is None):
#             continue
#         save_file(id_str, file_name, file_data, user_name)

#         files_list.append(file_name)
#     session["id"] = id_str
#     session["files_list"] = files_list
#     response_data = {'uuid': id_str}
    
#     return jsonify(response_data)

# def generate_request_id():
#     new_id = uuid.uuid4()
#     return new_id
