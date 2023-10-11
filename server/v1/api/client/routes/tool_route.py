from flask import Blueprint, request, session, jsonify, Response,redirect, url_for
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
submit_format = []

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
        
        file_status = {
            "file_id": extract_file_type(file_id),
            "file_name": file_name,
            "file_status": "Not started"
        }
        submit_format.append(file_status)
        
    session["id"] = id
    print("SESSION ID", session.get('id'))
    return jsonify(response_data)

results = {}
current_files_state={}
def analyze_file(user_name, id, file_id):        
    global current_files_state
    global submit_format
    resultFinalResult = Tool.analyze_single_file(
        args=
            ToolAnalyzeArgs(
                sub_container_file_path=f"{user_name}/{id}/contracts/",
                file_name=file_id,
            )
        )
    resultJson = obj_to_json(resultFinalResult)
    results[file_id] = resultJson
    current_files_state[file_id] = "Completed"
    for file in submit_format:
        if (file["file_id"] == extract_file_type(file_id)):
            file["file_status"] = "Completed"
    
    FlaskLog.info(f"current_file_state {current_files_state}")
    if all(state == "Completed" for state in current_files_state.values() ):
        current_files_state = {}
        submit_format = []
    create_file_doc_background( id=id, result=resultFinalResult)
    
count_enter = {}
@tool_route.route("/handle_results",methods=["GET"])
@cross_origin(supports_credentials=True)
def handle_result_id():
    print("file_id", file_id_queue)
    print("file_name", file_name_queue)
    user_name = "tung123"
    id_param = request.args.get('id')
    print("ID_PARAM", id_param)
    print("SESSION ID", session.get('id'))
    
    if not id_param:
        return "The 'id' query parameter is missing."
    if id_param not in count_enter:
        count_enter[id_param] = 0
    count_enter[id_param] +=1
    # if id_param == session.get('id'):
    submit_id = get_submit_by_id(id_param)
    print(f"submit_id {submit_id}")
    if (submit_id is not None):
        print(f"submit_id is {submit_id}")

        return redirect(url_for('client.tool_bp.handle_submit_id', id = id_param))    

    if count_enter[id_param] > 1:
        
        return redirect(url_for('client.tool_bp.handle_submit_id', id = id_param))    

    files_list =  get_all_files(id_param, user_name)
    for file_id in files_list:
        if file_id not in results:  
            thread = threading.Thread(target=analyze_file, args=(user_name, id_param, file_id))
            thread.start()
            current_files_state[file_id] = "Continue"
            for file in submit_format:
                if file["file_id"] == extract_file_type(file_id):
                    file["file_status"] = "Continue"

    return jsonify(submit_format)
    # return jsonify("Analyze started for files:\n" + "\n\t".join(files_list))


# Print out all session values
@tool_route.route('/print_session',methods=["GET"])
@cross_origin(supports_credentials=True)
def print_session():
    session_values = {key: session[key] for key in session}
    return jsonify(session_values)
    
@tool_route.route('/handle_file_id', methods=["GET"])
@cross_origin(supports_credentials=True)
def handle_file_id():
    id_param = request.args.get('id')
    
    FlaskLog.info(f"current_files_state: {current_files_state}")
    if id_param is None:
        return jsonify({"message:", "Missing file id param"})
    #NOTE: Neu dang tinh toan-> tra ve status

    file = get_file_by_id(id_param)
    if file is not None:
        file_dict = {
            "file_id": file.file_id,
            "file_name": file.file_name,
            "tool_name": file.tool_name,
            "duration": file.duration,
            "solc": file.solc,
            "analysis": file.analysis,
        }
        # file_json = obj_to_json(file_dict)  # Use indent for pretty formatting
        response = {"file_status": "Completed"}
        # file_tuple = [(key, value) for key, value in file_dict]
        response.update(file_dict)
        return response
    else:
        if id_param +'.sol' in current_files_state:
            for file in submit_format:
                print("File[file_id]", file["file_id"])
                print("file_id", id_param)
                if file["file_id"] == id_param:
                    return jsonify(file)
        # return jsonify({"file_state": current_files_state[id_param]}), 200
    
        return "File not found", 404  # Return a 404 Not Found status code

@tool_route.route('/handle_submit_id',methods=['GET'])
@cross_origin(supports_credentials=True)
def handle_submit_id():
    #TODO: Check if all file are done
    print("into handle submit id")
    id = request.args.get('id')
    print(id)
    if (current_files_state == {}):
        print("current_files_state is empty")
        submit_id =get_submit_by_id(id)
        if submit_id is None:
            return "submit_it doesn't exist", 404 # Return
            
        response_file = {}
        response_submit = []
        for file in submit_id:
            response_file = {
                "file_name": file.file_name,
                "file_id": file.file_id,
                "file_status": "Completed"
            }
            response_submit.append(response_file)
            
        return jsonify(response_submit)
    if any(value == "Continue" for value in current_files_state.values()):
        print("At least one file is not finished analyzing.")
    else:
        print("All files have been analyzed.")
    
    return jsonify(submit_format)
    # submit = get_submit_by_id(id_param)
    # FlaskLog.info(f"Submit {submit}")
    # files_json = {}
    # for file in submit:
    #     file_dict = {
    #         "file_id": file.file_id,
    #         "file_name": file.file_name,
    #         "tool_name": file.tool_name,
    #         "duration": file.duration,
    #         "solc": file.solc,
    #         "analysis": file.analysis,
    #         # Add more fields as needed
    #     }
    #     file_json = obj_to_json(file_dict)  # Use indent for pretty formatting
    #     files_json[file.file_name] = file_json
        
    # FlaskLog.info(f"current_file_state {current_files_state}")
    # return jsonify(files_json)

def create_file_doc_background(id, result:FinalResult) -> None:
    # Run create_file_doc asynchronously in a background thread
    thread = threading.Thread(target=create_file_doc, args=(id, result,))
    thread.start()
def generate_request_id():
    new_id = uuid.uuid4()
    return new_id
def get_all_files(id: str, username: str) -> list[str]:
    files_path = os.path.join(server.v1.config.app_config.get_local_storage_path(), username, id, "contracts")
    file_list = os.listdir(files_path)
    
    return file_list
def create_file_doc(id, result: FinalResult) -> list[str]:
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
        submit_id=id,
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
def extract_file_type(file_id) ->str:
    filename = os.path.basename(file_id)
    name_without_extension, _ = os.path.splitext(filename)
    return name_without_extension
    