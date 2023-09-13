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
import threading
def create_file_doc_background(result):
    # Run create_file_doc asynchronously in a background thread
    thread = threading.Thread(target=create_file_doc, args=(result,))
    thread.start()
    
def handle_tool():
    user_name = "phu21122003"
    tools = ["Mythril", "Slither"]
    if request is None:
        return jsonify({"message": "Nothing requested"}), StatusCode.BadRequest.value
    
    files_data = request.files
    file_keys = files_data.keys()
    file_list = []
    
    for file_key in file_keys:
        file_data = files_data[file_key]
        file_name = file_data.filename
        save_file(file_name, file_data, user_name)
        
        file_list.append(file_name)
    
    FlaskLog.info(f"{file_list} {tools}  {user_name}")
    result = Tool.run_tools(file_list, tools, user_name)
    add_issue_ids(result)
    create_file_doc_background(result)    
    
    return jsonify(result), StatusCode.OK.value

