from dataclasses import dataclass
from enum import Enum, unique
from typing import List

@unique
class ToolName(Enum):
    Mythril = "mythril"
    Slither = "slither"

@unique
class ErrorClassification(Enum):
    RuntimeOut = "runtime out"
    CompileError = "compile error"
    UnsupportedSolc = "unsupported solc"
    UndefinedSolc = "undefined solc"
    UnknownError = "unknown error"

@dataclass
class AnalysisError:
    error_title: str
    line_no: int
    start_char_idx: int
    description: str
    typeDetect: str
@dataclass
class ToolError:
    error: ErrorClassification
    msg: str | List[AnalysisError] 
    
@dataclass
class AnalysisIssue:
    contract: str
    source_map: str
    line_no: list[int]
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
    #combine here
    issues: list[AnalysisIssue]

@dataclass
class FinalResult:
    file_name: str
    tool_name: str
    duration: float
    solc: str
    analysis: AnalysisResult


@dataclass
class ImageVolume:
    bind: str
    mode: str
@dataclass
class ImageConfig:
    docker_image: str
    analyze_cmd: str
    options: str
    volumes: ImageVolume
    timeout: int

@dataclass
class ToolAnalyzeArgs:
    sub_container_file_path: str
    file_name: str
    solc: str = ""
    docker_image: str = ""
    options: str = ""
    timeout: int = -1
