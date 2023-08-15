from tools.Tool import Tool, RawResult, FinalResult
# from type import FinalResult, ToolError, ToolName, IssueType,SlitherAnalysisDetector, SlitherAnalysisDetectorElement
from tools.type import *
class Slither(Tool):
    
    tool_name = ToolName.Slither
    
    def __init__(self):
        pass
    
    @classmethod
    def parse_raw_result(
            cls, 
            raw_result: dict, 
            duration: float = "1", file_name: str = "1") -> FinalResult:
        if not raw_result["success"]:
            return raw_result["error"]
        
        issues = list(SlitherAnalysisDetector)   
        for detectors in raw_result["detectors"]:
            issue = SlitherAnalysisDetector(
                detectors["check"],
                detectors["confidence"],
                detectors["impact"],
                detectors["description"]
            ) 
            
            for element in detectors["elements"]:
                _element = SlitherAnalysisDetectorElement(
                    element["type"], 
                    element["name"], 
                    element["lines"], 
                    element["directive"])
                issue.elements.append(_element)

            issues.append(issue)

# print(Slither.parse_raw_result('../../PittyTest/output.json'))
    