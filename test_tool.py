import sys
import os
from server.v1.api.utils.StatusCode import StatusCode
# from tools.Slither import Slither

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# g: FinalResult = Tool.analyze_files_async(
#     files=[
#         ToolAnalyzeArgs(
#             sub_container_file_path="user1/contracts",
#             file_name="swc-106.sol",
#             # solc="0.4.13"
#         )
#     ],
#     tools=[ToolName.Slither, ToolName.Mythril]
# )

# print(g)
print((StatusCode.BadRequest.value))
