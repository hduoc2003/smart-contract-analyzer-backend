from flask import Blueprint, request, session, jsonify, Response
from flask_session import Session
from flask_cors import CORS, cross_origin
from tools.Tool import Tool
from server.v1.api.utils.StatusCode import StatusCode
from server.v1.api.utils.FlaskLog import *
from server.v1.api.client.models.tools_collection import *
import threading
from werkzeug.datastructures.file_storage import FileStorage
from werkzeug.datastructures.structures import ImmutableMultiDict
from _collections_abc import dict_keys
from tools.types import ToolAnalyzeArgs
from tools.utils.parsers import obj_to_jsonstr, obj_to_json
from tools.types import FinalResult
from typing import Generator
from flask import current_app
from server.v1.api.utils.StatusCode import StatusCode

tool_route = Blueprint("tool_bp", __name__, url_prefix="/tool")

file_name_queue = []
file_id_queue = []
@tool_route.route("/handle_files",methods=["POST"])
@cross_origin(supports_credentials=True)
def handle_files():
    user_name = "tung123"
    id = str(generate_request_id())
        
    if request is None:
        return jsonify({"message": "Nothing requested"}), StatusCode.BadRequest.value
    
    files_data: ImmutableMultiDict[str, FileStorage] = request.files
    file_keys: dict_keys[str, FileStorage] = files_data.keys()
    
    response_data = {'uuid': id}

    for file_key in file_keys:
        file_data: FileStorage = files_data[file_key]
        file_id: str = str(generate_request_id())
        file_name: str | None = file_data.filename
        if (file_name is None):
            continue
        save_file(id, file_id, file_data, user_name)
        response_data[file_name] = file_id
        file_name_queue.append(file_name)
        file_id_queue.append(file_id)
        
    session["id"] = id

    print("SESSION ID", session.get('id'))

    return jsonify(response_data)

@tool_route.route("/handle_results",methods=["GET"])
@cross_origin(supports_credentials=True)
def handle_get_result_id():
    if request.method == "GET":
        # Handle the GET request here
        return "This is a GET request."

@tool_route.route("/handle_results",methods=["POST"])
@cross_origin(supports_credentials=True)
def handle_result_id():
    print("HANDLE ID")
    user_name = "tung123"

    id_param = request.args.get('id')
    print("ID_PARAM", id_param)
    print("SESSION ID", session.get('id'))
    if not id_param:
        return "The 'id' query parameter is missing."
    if id_param != session.get('id'):
        return "Nope wrong id matching", 400

    files_list =  get_all_files(id_param, user_name)
    print("files_list", files_list)
    result_stream: Generator = Tool.analyze_files_async(
        files=[
            ToolAnalyzeArgs(
                sub_container_file_path=f"{user_name}/{id_param}/contracts/",
                file_name=file_name,
            ) for file_name in files_list
        ],
        stream=True
    ) # type: ignore
    def temp() -> Generator[str, Any, None]:
        for final_result in result_stream:
            # final_result: FinalResult
            final_result.file_id = file_id_queue[0]
            final_result.file_name = file_name_queue[0]
            create_file_doc_background(final_result)
            
            yield obj_to_jsonstr(final_result)
    session.pop('id', None)
    # session.pop('files_list', None)
    return Response(temp())


# Print out all session values
@tool_route.route('/print_session',methods=["GET"])
@cross_origin(supports_credentials=True)
def print_session():
    session_values = {key: session[key] for key in session}
    return jsonify(session_values)


def create_file_doc_background(result:FinalResult) -> None:
    # Run create_file_doc asynchronously in a background thread
    thread = threading.Thread(target=create_file_doc, args=(result,))
    thread.start()
def generate_request_id():
    new_id = uuid.uuid4()
    return new_id

def get_all_files(id: str, username: str) -> list[str]:
    files_path = os.path.join(server.v1.config.app_config.get_local_storage_path(), username, id, "contracts")
    file_list = os.listdir(files_path)

    return file_list
    
    

@tool_route.route('/handle_file_id', methods=["GET"])
@cross_origin(supports_credentials=True)
def handle_file_id():
    id_param = request.args.get('id')
    file = get_file_by_id(id_param)
    
    if file is not None:
        file_dict = {
            "file_id": file.file_id,
            "file_name": file.file_name,
            "tool_name": file.tool_name,
            "duration": file.duration,
            "solc": file.solc,
            "analysis": file.analysis,
            # Add more fields as needed
        }
        file_json = obj_to_json(file_dict)  # Use indent for pretty formatting
        return file_json
    else:
        return "File not found", 404  # Return a 404 Not Found status code
def create_file_doc(result: FinalResult) -> list[str]:
    # (file_name, tool_name, duration, analysis) = extract_file_res(result)
    file_name = result.file_name
    tool_name = result.tool_name
    duration = result.duration
    solc = result.solc
    analysis = result.analysis
    issues = []
    count = 0
    files_id: list[str] = [] 
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
    new_file = FileDoc(
        file_id=file_id_queue.pop(0),
        file_name=file_name_queue.pop(0),
        tool_name=tool_name,
        duration=duration,
        solc = solc,
        analysis=[
            {
                "errors": analysis.errors
            },
            {
                "issues": issues
            }
        ]
    )
    new_file.save()
    return files_id
