import logging
from flask import Flask, jsonify, request
from typing import Any, List
import tempfile
import os
from tools.Tool import Tool, ToolName
from server.v1.api.utils.StatusCode import StatusCode
from server.v1.api.utils.FlaskLog import *
import server.v1.config.app_config
import json
from bson import ObjectId  # Import ObjectId for generating unique IDs
from server.v1.api.client.models.tools_collection import *

def handle_tool():
    user_name = "phu21122003"
    tools = ["Mythril", "Slither"]
    if request is None:
        return jsonify({"message": "Nothing requested"}), StatusCode.BadRequest.value
    
    files_data = request.files
    file_keys = files_data.keys()
    
    print(file_keys)
    file_list = []
    for file_key in file_keys:
        file_data = files_data[file_key]
        file_name = file_data.filename
        file_content = file_data.read()
        
        # Save the file to local storage
        save_file_to_local_storage(file_name, file_content, user_name)
        
        file_list.append(file_name)
    
    print("FILELIST: ", file_list)

    FlaskLog.info(f"{file_list} {tools}  {user_name}")
    result = Tool.run_tools(file_list, tools, user_name)
    
    result_dict = str_to_dict(result)

    create_file_doc(result_dict)
    
    add_issue_ids(result_dict)
    return jsonify(result_dict), StatusCode.OK.value

