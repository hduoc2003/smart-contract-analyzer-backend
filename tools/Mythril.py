import json
from math import e
from tools.Tool import Tool
from tools.Tool import FinalResult
from tools.Tool import RawResult
from tools.type import AnalysisIssue, AnalysisResult, ErrorClassification, ToolError, ToolName
from tools.utils.SWC import get_swc_link, get_swc_title, valid_swc

class Mythril(Tool):

    tool_name = ToolName.Mythril

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def parse_raw_result(cls, raw_result: RawResult, duration: float, file_name: str) -> FinalResult:

        issues: list[AnalysisIssue] = []
        for raw_issue in raw_result['issues']:
            (is_valid_swc, swcID) = valid_swc(raw_issue['swc-id'])
            contract=raw_issue['contract']
            if (not is_valid_swc):
                raise Exception(f"{contract} in {file_name} has wrong swc-id: {swcID}")
            issues.append(AnalysisIssue(
                contract=contract,
                source_map=raw_issue['sourceMap'],
                line_no=raw_issue['lineno'],
                code=raw_issue['code'],
                description=raw_issue['description'],
                hint="chưa làm phần hint",
                issue_title=raw_issue['title'],
                swcID=swcID,
                swc_title=get_swc_title(swcID, validated=True),
                swc_link=get_swc_link(swcID, validated=True),
                severity=raw_issue['severity']
            ))

        final_result = FinalResult(
            file_name=file_name,
            tool_name=Mythril.tool_name.value,
            duration=duration,
            analysis=AnalysisResult(
                errors=[],
                issues=issues
            )
        )
        return final_result

    @classmethod
    def parse_error_result(cls, errors: list[ToolError], duration: float, file_name: str) -> FinalResult:
        final_result = FinalResult(
            file_name=file_name,
            tool_name=Mythril.tool_name.value,
            duration=duration,
            analysis=AnalysisResult(
                errors=errors,
                issues=[]
            )
        )
        return final_result

    @classmethod
    def detect_errors(cls, raw_result_str: str) -> list[ToolError]:
        raw_result_json = json.loads(raw_result_str)
        errors: list[ToolError] = []
        raw_result_errors = raw_result_json['error']
        if (isinstance(raw_result_errors, str) and
            raw_result_json['error'].find("Solc experienced a fatal error") != -1
        ):
            errors.append(ToolError(
                error=ErrorClassification.CompileError,
                msg=raw_result_json['error']
            ))
        return errors

