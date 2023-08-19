import asyncio
from concurrent.futures import ThreadPoolExecutor
import sys
import os
import pathlib
import json
import time
from tools.Mythril import Mythril
from tools.Tool import Tool

from tools.docker.Docker import Docker
from tools.type import ToolName
from tools.utils.Async import Async
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

start = time.time()
result = [t for t in (Tool.analyze_files_async(
    file_dir_path=r'D:\SE_LAB\SE_Task\blockchain\tool\test-mythril\bugs',
    files_names=['swc-106.sol']*1,
    tools=[ToolName.Mythril]
))]
end = time.time()

print(end - start)
print(result)


# print(Mythril.tool_cfg)
