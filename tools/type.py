from dataclasses import dataclass
from enum import Enum, unique
from typing import List, Union

@unique
class ToolName(Enum):
    Mythril = "mythril"
    Slither = "slither"

@unique
class ErrorClassification(Enum):
    RuntimeOut = "runtime out"
    CompileError = "compile error"
    UnknownError = "unknown error"
 
@dataclass
class ToolError:
    error: ErrorClassification
    msg: str

@dataclass
class AnalysisIssue:
    contract: str #slither
    source_map: str #slither
    line_no: str #slither
    source_mapping: 
    code: str #??
    description: str #slither
    hint: str
    issue_title: str
    swcID: str
    swc_title: str
    swc_link: str
    severity: str

@dataclass
class AnalysisResult:
    errors: list[ToolError]
    #combine here
    issues: list[AnalysisIssue]
    
@dataclass
class FinalResult:
    file_name: str
    tool_name: str
    duration: float
    analysis: AnalysisResult


@dataclass
class SlitherDetectorElement:
    type: str #[check] property in raw object
    name: str
    lines_no: list[int]
    contract: str #find by contractFinderFunction
#     For function/event type elements:
# parent (result-element): Refers to the parent contract of this definition.
# signature (string): Refers to the full signature of this function
# For enum/struct type elements:
# parent (result-element): Refers to the parent contract of this definition.
# For variable type elements:
# parent (result-element): Refers to the parent contract if this variable is a state variable. Refers to the parent function if this variable is a local variable.
# For node type elements:
# parent (result-element): Refers to the parent function of this node.
# For pragma type elements:
# directive (string array): Fully serialized pragma directive (ie: ["solidity", "^", "0.4", ".9"])
    hint: str
    sample_code: str
    additional_fields: dict
       
@dataclass
class SlitherDetector:
    detect_type: str
    impact: str
    confidence: str
    description: str
    elements: list[SlitherDetectorElement]
    
@dataclass
class SlitherUpgradeability:

    
    