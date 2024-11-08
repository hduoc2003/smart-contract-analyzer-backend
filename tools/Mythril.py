import json
import os
import subprocess
from sys import stdout
import traceback
from typing_extensions import override

from tools.Tool import Tool
from tools.Tool import FinalResult
from tools.Tool import RawResult
from tools.tool_types import AnalysisIssue, AnalysisResult, ErrorClassification, ToolAnalyzeArgs, ToolError, ToolName
from tools.utils.Log import Log
from tools.utils.SWC import get_swc_link, get_swc_title, valid_swc

class Mythril(Tool):

    tool_name = ToolName.Mythril
    tool_cfg = Tool.load_default_cfg(tool_name)
    tool_exec_path = os.path.join(os.path.dirname(__file__), 'mythril_venv/bin/myth')

    def __init__(self) -> None:
        super().__init__()

    @override
    @classmethod
    def parse_raw_result(cls, raw_result: RawResult, duration: float, file_name: str, solc: str) -> FinalResult:

        issues: list[AnalysisIssue] = []
        if (isinstance(raw_result, dict)) and ('issues' in raw_result):
            for raw_issue in raw_result['issues']:
                (is_valid_swc, swcID) = valid_swc(raw_issue['swc-id'])
                contract=raw_issue['contract']
                if (not is_valid_swc):
                    raise Exception(f"{contract} in {file_name} has wrong swc-id: {swcID}")
                try:
                    issues.append(AnalysisIssue(
                    contract=contract,
                    source_map=parse_source_map(raw_issue['sourceMap']),
                    line_no=raw_issue['lineno'] if 'lineno' in raw_issue else [0],
                    code=raw_issue['code'] if 'code' in raw_issue else "",
                    description=raw_issue['description'],
                    hint= "chưa làm phần hint",
                    issue_title=raw_issue['title'],
                    swcID=swcID,
                    swc_title=get_swc_title(swcID, validated=True),
                    swc_link=get_swc_link(swcID, validated=True),
                    severity=raw_issue['severity']
                ))
                except Exception as e:
                    print('error raw_issue: ', raw_issue)
                    traceback.print_exc()
                    raise e

        final_result = FinalResult(
            file_name=file_name,
            tool_name=Mythril.tool_name.value,
            duration=duration,
            solc=solc,
            analysis=AnalysisResult(
                errors=[],
                issues=issues
            )
        )
        return final_result

    @override
    @classmethod
    def parse_error_result(cls, errors: list[ToolError], duration: float, file_name: str, solc: str) -> FinalResult:
        final_result = FinalResult(
            file_name=file_name,
            tool_name=Mythril.tool_name.value,
            duration=duration,
            solc=solc,
            analysis=AnalysisResult(
                errors=errors,
                issues=[]
            )
        )
        return final_result

    @override
    @classmethod
    def detect_errors(cls, raw_result_str: str) -> list[ToolError]:
        errors: list[ToolError] = []
        try:
            raw_result_json = json.loads(raw_result_str)
        except Exception:
            Log.info(f'Failed when parsing raw_result_json in function detect_errors:\n{raw_result_str}')
            errors.append(ToolError(
                error=ErrorClassification.UnknownError,
                msg=raw_result_str
            ))
            return errors

        raw_result_errors = raw_result_json['error']
        if (isinstance(raw_result_errors, str)):
            if (raw_result_errors.find('Source file requires different compiler version') != -1):
                errors.append(Tool.get_tool_error(
                    ErrorClassification.UnsupportedSolc
                ))
            elif (raw_result_errors.find("Solc experienced a fatal error") != -1):
                errors.append(ToolError(
                    error=ErrorClassification.CompileError,
                    msg=raw_result_errors
                ))
            elif (raw_result_errors.find('solcx.exceptions.UnsupportedVersionError') != -1):
                errors.append(Tool.get_tool_error(
                    ErrorClassification.UnsupportedSolc
                ))
            else:
                errors.append(ToolError(
                    error=ErrorClassification.UnknownError,
                    msg=raw_result_errors
                ))
        return errors

    @override
    @classmethod
    def run_core(
        cls,
        args: ToolAnalyzeArgs
    ) -> tuple[list[ToolError], str]:
        if (args.options.find(r"{solc}") != -1):
            args.options = args.options.replace(r"{solc}", args.solc)

        errors: list[ToolError] = []
        logs: str = ""
        # container_file_path = f"{cls.tool_cfg.volumes.bind}/{args.sub_container_file_path}"
        container_file_path = f"{Tool.storage_path}/{args.sub_container_file_path}"
        cmd = f"{cls.tool_exec_path} analyze {container_file_path}/{args.file_name} {args.options} --execution-timeout {args.timeout}"
        # print(cmd)
        # print("CONTAINER ", cls.container)
        result = subprocess.run(cmd.split(" "), capture_output=True, text=True)
        print('out:', result.stdout)
        print('err:', result.stderr)
        logs = result.stdout if len(result.stdout) > 0 else result.stderr
        # if (len(logs) == 0):
        #     errors.append(ToolError(
        #         error=ErrorClassification.RuntimeOut,
        #         msg=f"Timeout while analyzing {container_file_path}/{args.file_name} using Mythril: timeout={args.timeout}"
        #     ))

        return (errors, logs)

def parse_source_map(source_map) -> str:
    if not isinstance(source_map, str):
        return "0:0"
    src_map_shorten = source_map[:4]
    return src_map_shorten
