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
    contract: str 
    source_map: str 
    line_no: list[int] | int
    code: str #??
    description: str 
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
    contract: str
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
    
# @dataclass
# class SlitherUpgradeability:
