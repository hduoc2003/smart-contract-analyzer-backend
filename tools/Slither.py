from tools.Tool import Tool, RawResult, FinalResult
# from type import FinalResult, ToolError, ToolName, IssueType,SlitherAnalysisDetector, SlitherAnalysisDetectorElement
from tools.type import *
class Slither(Tool):
    
    tool_name = ToolName.Slither
    
    def __init__(self):
        super().__init__()
    
    @classmethod
    def parse_raw_result_to_dict(
            cls, 
            raw_result: dict, 
            duration: float = 1, file_name: str = "1"):
        # if not raw_result["success"]:
        #     return raw_result["error"]
        
        # issues: list[SlitherDetector] =[]   
        # for detectors in raw_result["detectors"]:
        #     elements: dict = {}
        #     for element in detectors["elements"]:
        #         _element = SlitherAnalysisDetectorElement(
        #             element["type"], 
        #             element["name"], 
        #             element["lines"], 
        #             element["directive"])
            
        #     issues.append(issue)'
        pass
        

    @classmethod
    def find_contract(cls):
        pass
    
    
# print(Slither.parse_raw_result('../../PittyTest/output.json'))
    