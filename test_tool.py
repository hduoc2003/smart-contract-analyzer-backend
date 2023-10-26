import sys
import os
import time
from server.v1.api.utils.Async import Async
from tools.Tool import Tool
from tools.types import ToolAnalyzeArgs, ToolName
from tools.utils.parsers import obj_to_jsonstr
# from tools.Slither import Slither

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

g = Tool.analyze_files_async(
    files=[
        ToolAnalyzeArgs(
            sub_container_file_path="user1/contracts",
            file_name="swc-101.sol",
            # solc="0.4.13"
        )
    ],
    tools=[ToolName.Slither, ToolName.Mythril]
)

print(obj_to_jsonstr(g[0])) # type: ignore
