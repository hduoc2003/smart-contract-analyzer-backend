from venv import logger
from flask import Blueprint, request

from tools.utils.Log import Log

tool_route = Blueprint("tool", __name__, url_prefix="/tool")

@tool_route.post("/")
def response():
    saved_file_dir: str = r'D:\SE_LAB\SE_Task\blockchain\tool\test-mythril\bugs'
    files_names: list[str] = ['swc-107.sol', 'swc-117.sol']


    return "hehe"
