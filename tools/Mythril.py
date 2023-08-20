import json
from pydoc import doc
from typing_extensions import override

import requests
from tools.Tool import Tool
from tools.Tool import FinalResult
from tools.Tool import RawResult
from tools.docker.Docker import Docker
from tools.type import AnalysisIssue, AnalysisResult, ErrorClassification, ToolError, ToolName
from tools.utils.Log import Log
from tools.utils.SWC import get_swc_link, get_swc_title, valid_swc

class Mythril(Tool):

    tool_name = ToolName.Mythril
    tool_cfg = Tool.load_default_cfg(tool_name)

    def __init__(self) -> None:
        super().__init__()

    @override
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
                hint= "chưa làm phần hint",
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

    @override
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
                errors.append(ToolError(
                    error=ErrorClassification.UnsupportedSolc,
                    msg="We only support Solidity from version 0.4.11, please use Solidity newer version in source code"
                ))
            elif (raw_result_errors.find("Solc experienced a fatal error") != -1):
                errors.append(ToolError(
                    error=ErrorClassification.CompileError,
                    msg=raw_result_errors
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
        container_file_path: str,
        file_name: str,
        docker_image: str,
        options: str,
        timeout: int
    ) -> tuple[list[ToolError], str]:
        errors: list[ToolError] = []
        logs: str = ""
        cmd = f"{cls.tool_cfg.analyze_cmd} {container_file_path}/{file_name} {options}"
        container = Docker.client.containers.run(
            image=docker_image,
            command=cmd,
            detach=True,
            volumes=Docker.create_volumes(
                [Tool.storage_path],
                [cls.tool_cfg.volumes.bind]
            )
        )
        try:
            container.wait(timeout=timeout) # type: ignore
        except requests.exceptions.ConnectionError as e:
            Log.info('#####################')
            errors.append(ToolError(
                error=ErrorClassification.RuntimeOut,
                msg=f"Time out while running image {docker_image} to analyze {file_name}"
            ))
            Log.err(f"Time out while running image {docker_image} to analyze {file_name}")
            Log.print_except(e)


        # print(container.logs().decode("utf8"))
        logs: str = container.logs().decode("utf8").strip() # type: ignore
        # Log.info(logs)
        #if My
        container.remove() # type: ignore

        return (errors, logs)
