import json
from math import e
from typing import Container
from typing_extensions import override
from tools.Tool import Tool
from tools.Tool import FinalResult
from tools.Tool import RawResult
from tools.docker.Docker import Docker
from tools.type import AnalysisIssue, AnalysisResult, ErrorClassification, ToolAnalyzeArgs, ToolError, ToolName
from tools.utils.Log import Log
from tools.utils.SWC import get_swc_link, get_swc_title, link_hint, map_slither_check_to_swc,get_swc_no


class Slither(Tool):

    tool_name = ToolName.Slither
    tool_cfg = Tool.load_default_cfg(tool_name)
    container_name = "slither-tool"

    # create container
    container = Docker.client.containers.get(container_name) \
            if Docker.exists_container(container_name) \
            else Docker.client.containers.run(
                image=tool_cfg.docker_image,
                command="",
                detach=True,
                name=container_name,
                tty=True,
                volumes=Docker.create_volumes(
                    host_paths=[Tool.storage_path],
                    container_paths=[tool_cfg.volumes.bind]
                )
            )
    container.start() # type: ignore

    # load solcs
    not_installed_solcs = Docker.exec_run(
        container=container,
        cmd="solc-select install"
    ).output.decode("utf8").replace("Available versions to install:", "").split()
    if (len(not_installed_solcs) > 0):
        Log.info("Installing solcs for Slither...")
        for solc in not_installed_solcs:
            Docker.exec_run(
                container=container,
                cmd=f"solc-select install {solc}",
                detach=True
            )

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def get_smallest_element(cls, elements: list[dict]) -> dict:
        if (len(elements) == 0):
            return {}
        elif (len(elements) == 1):
            return elements[0]
        else:
            for element in elements:
                # TODO:will add more
                if element["type"] == "node":
                    return element
        return elements[0]

    # comment
    @staticmethod
    def get_contract(element: dict) -> str:
        if (element == {}): return ''
        if element.get("type") == "pragma":
            return ""
        else:
            if element.get("type") == "contract":
                return element["name"]
            else:
                # print (element["type_specific_fields"]
                #                                 ["parent"])
                contract = Slither.get_contract(element["type_specific_fields"]
                                                ["parent"])
                return contract

    @staticmethod
    def convert_source_map_represent(source_map: dict) -> str:
        start = source_map["start"]
        len = source_map["length"]
        return f'{start}:{len}:0'

    @classmethod
    def parse_raw_result(cls, raw_result: RawResult, duration: float, file_name: str, solc: str) -> FinalResult:
        issues: list[AnalysisIssue] = []
        detectors = raw_result["results"]["detectors"]
        for detector in detectors:
            elements = detector.get("elements")
            element = Slither.get_smallest_element(elements)
            swcID= get_swc_no(detector['check'])
            issue = AnalysisIssue(
                contract= Slither.get_contract(element) if element else "",
                source_map= Slither.convert_source_map_represent(element["source_mapping"]) if element else "",
                line_no=element["source_mapping"]["lines"] if element else [],
                code="Không có source code :(, FE tự điền ứng với sourcemap nhé",
                description=detector['description'] ,
                hint= link_hint(detector["check"]),
                issue_title= detector['check'],
                swcID= swcID,
                swc_title=get_swc_title(swcID),
                swc_link=get_swc_link(swcID),
                severity= detector['impact']
            )
            issues.append(issue)

        final_result = FinalResult(
            file_name=file_name,
            tool_name=Slither.tool_name.value,
            duration = duration,
            solc=solc,
            analysis=AnalysisResult(
                errors=[],
                issues= issues
            )
        )
        return final_result
    @classmethod
    def parse_error_result(cls, errors: list[ToolError], duration: float, file_name: str, solc:str) -> FinalResult:
        final_result = FinalResult(
            file_name=file_name,
            tool_name=Slither.tool_name.value,
            duration=duration,
            solc=solc,
            analysis=AnalysisResult(
                errors=errors,
                issues=[]
            )
        )
        return final_result

    @classmethod
    def detect_errors(cls, raw_result_str: str) -> list[ToolError]:
        errors: list[ToolError] = []
        try:
            raw_result_json = json.loads(raw_result_str)
        except Exception as e:
            Log.info(f'Failed when parsing raw_result_json in function detect_errors:\n{raw_result_str}')
            errors.append(ToolError(
                error=ErrorClassification.UnknownError,
                msg=raw_result_str
            ))
            return errors
        raw_result_errors = raw_result_json["error"]
        print(raw_result_errors)
        if (isinstance(raw_result_errors, str)):
            if (raw_result_errors.find('Source file requires different compiler version') != -1):
                errors.append(Tool.get_tool_error(
                    error=ErrorClassification.UnsupportedSolc,
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
        args: ToolAnalyzeArgs
    ) -> tuple[list[ToolError], str]:
        if (args.options.find(r"{solc}") != -1):
            args.options = args.options.replace(r"{solc}", args.solc)
        errors: list[ToolError] = []
        logs: str = ""
        container_file_path = f"{cls.tool_cfg.volumes.bind}/{args.sub_container_file_path}"
        cmd = f"timeout {args.timeout}s {cls.tool_cfg.analyze_cmd} {container_file_path}/{args.file_name} {args.options}"
        # print(cmd)

        logs = Docker.exec_run(
            container=cls.container,
            cmd=cmd
        ).output.decode("utf8")

        if (len(logs) == 0):
            errors.append(ToolError(
                error=ErrorClassification.RuntimeOut,
                msg=f"Timeout while analyzing {container_file_path}/{args.file_name} using Slither: timeout={args.timeout}"
            ))
        return (errors, logs)