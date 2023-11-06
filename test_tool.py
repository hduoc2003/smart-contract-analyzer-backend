import datetime
from re import sub
import sys
import os
import time
from server.v1.api.utils.dict_utils import exclude_fields, include_fields
from server.v1.api.utils.path import get_all_files
from tools.Tool import Tool
from tools.types import ToolAnalyzeArgs, ToolName
from tools.utils.Async import Async
from tools.utils.parsers import obj_to_json, obj_to_jsonstr
# from tools.Slither import Slither

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# files = get_all_files(r'D:\SE_LAB\SE_Task\blockchain\tool\smart-contract-analyzer\smart-contract-analyzer-backend\tools\storage\user1\contracts')
# files = ['shadowing_variable.sol', 'swc-107-reentrancy-eth.sol']

# lengths = [len(g.analysis.issues) for g in Tool.analyze_files_async(
#     files=[ToolAnalyzeArgs(
#         sub_container_file_path='user1/contracts',
#         file_name=file_name
#     ) for file_name in files]
# )]

# for i in range(0, 50):
#     temp = [len(g.analysis.issues) for g in Tool.analyze_files_async(
#         files=[ToolAnalyzeArgs(
#             sub_container_file_path='user1/contracts',
#             file_name=file_name
#         ) for file_name in files]
#     )]

#     done = False
#     for i, length in enumerate(temp):
#         if (temp[i] != lengths[i]):
#             print(f'file: {files[i]}\ntemp[i]: {temp[i]}\nlengths[i]: ${lengths[i]}')
#             done = True
#             break
#     if (done):
#         break

a = {
    'a': 1,
    'b': 2,
}

print(datetime.datetime.now())
