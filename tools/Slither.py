import json
from math import e
from typing import Container
from typing_extensions import override
from tools.Tool import Tool
from tools.Tool import FinalResult
from tools.Tool import RawResult
from tools.docker.Docker import Docker
from tools.type import AnalysisIssue, AnalysisResult, ErrorClassification, ToolError, ToolName
from tools.utils.Log import Log
from tools.utils.SWC import get_swc_link, get_swc_title, link_hint, map_slither_check_to_swc,get_swc_no


class Slither(Tool):

    tool_name = ToolName.Slither
    tool_cfg = Tool.load_default_cfg(tool_name)
    valid_solcs: list[str] = ['0.8.21', '0.8.20', '0.8.19', '0.8.18', '0.8.17', '0.8.16', '0.8.15', '0.8.14', '0.8.13', '0.8.12', '0.8.11', '0.8.10', '0.8.9', '0.8.8', '0.8.7', '0.8.6', '0.8.5', '0.8.4', '0.8.3', '0.8.2', '0.8.1', '0.8.0', '0.7.6', '0.7.5', '0.7.4', '0.7.3', '0.7.2', '0.7.1', '0.7.0', '0.6.12', '0.6.11', '0.6.10', '0.6.9', '0.6.8', '0.6.7', '0.6.6', '0.6.5', '0.6.4', '0.6.3', '0.6.2', '0.6.1', '0.6.0', '0.5.17', '0.5.16', '0.5.15', '0.5.14', '0.5.13', '0.5.12', '0.5.11', '0.5.10', '0.5.9', '0.5.8', '0.5.7', '0.5.6', '0.5.5', '0.5.4', '0.5.3', '0.5.2', '0.5.1', '0.5.0', '0.4.26', '0.4.25', '0.4.24', '0.4.23', '0.4.22', '0.4.21', '0.4.20', '0.4.19', '0.4.18', '0.4.17', '0.4.16', '0.4.15', '0.4.14', '0.4.13', '0.4.12', '0.4.11', '0.4.10', '0.4.9', '0.4.8', '0.4.7', '0.4.6', '0.4.5', '0.4.3', '0.4.2', '0.4.1', '0.4.0']
    solc_solcs_select = ",".join(valid_solcs)
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
    def parse_raw_result(cls, raw_result: RawResult, duration: float, file_name: str) -> FinalResult:
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
            analysis=AnalysisResult(
                errors=[],
                issues= issues
            )
        )
        return final_result
    @classmethod
    def parse_error_result(cls, errors: list[ToolError], duration: float, file_name: str) -> FinalResult:
        final_result = FinalResult(
            file_name=file_name,
            tool_name=Slither.tool_name.value,
            duration=duration,
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
        if (isinstance(raw_result_errors, str)):
            if (raw_result_errors.find("Solc experienced a fatal error") != -1):
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
        timeout: int,
    ) -> tuple[list[ToolError], str]:
        if (options.find(r"{solcs}") != -1):
            options = options.replace(r"{solcs}", cls.solc_solcs_select)
        errors: list[ToolError] = []
        logs: str = ""
        cmd = f"timeout {timeout}s {cls.tool_cfg.analyze_cmd} {container_file_path}/{file_name} {options}"
        # print(cmd)

        logs = Docker.exec_run(
            container=cls.container,
            cmd=cmd
        ).output.decode("utf8")

        if (len(logs) == 0):
            errors.append(ToolError(
                error=ErrorClassification.RuntimeOut,
                msg=f"Timeout while analyzing {container_file_path}/{file_name} using Slither: timeout={timeout}"
            ))
        return (errors, logs)
