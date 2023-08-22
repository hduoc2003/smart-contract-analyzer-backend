import asyncio
from concurrent.futures import ThreadPoolExecutor
import sys
import os
import pathlib
import json
import time
from tools.Mythril import Mythril
from tools.Slither import Slither
# from tools.Slither import Slither
from tools.Tool import Tool

from tools.type import FinalResult, ToolAnalyzeArgs, ToolName
from tools.utils.parsers import obj_to_jsonstr
from tools.docker.Docker import Docker
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

g: FinalResult = Tool.analyze_files_async(
    files=[
        ToolAnalyzeArgs(
            sub_container_file_path="user1/contracts",
            file_name="swc-106.sol",
            # solc="0.4.13"
        )
    ],
    tools=[ToolName.Slither, ToolName.Mythril]
)

print(g)
