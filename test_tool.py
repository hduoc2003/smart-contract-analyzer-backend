from tools.Tool import Tool
from tools.Slither import Slither
from tools.tool_types import ToolAnalyzeArgs, ToolName

g = Tool.analyze_files_async(
    files=[ToolAnalyzeArgs(
        sub_container_file_path='tung123/e5f485c3-f330-4cd4-bdfd-bde997e03d54/contracts',
        file_name='665c5a87-07e6-4557-a77d-403835139119.sol'
    )],
    tools=[ToolName.Mythril]
)

print(g)

