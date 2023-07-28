from dataclasses import dataclass
from enum import Enum, unique

@unique
class ToolName(Enum):
        Mythril = "mythril"
        Slither = "slither"

@unique
class ErrorClassification(Enum):
    RuntimeOut = "runtime out"
    CompileError = "compile error"

@dataclass
class ToolError:
    error: ErrorClassification
    msg: str

@dataclass
class AnalysisIssue:
    contract: str
    source_map: str
    line_no: str
    code: str
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
    issues: list[AnalysisIssue]

@dataclass
class FinalResult:
    file_name: str
    tool_name: str
    duration: float
    analysis: AnalysisResult
