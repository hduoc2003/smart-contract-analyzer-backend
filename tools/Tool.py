from abc import ABC, abstractmethod
import json
import os
from time import time
from typing import Any
from tools.type import FinalResult, ToolError, ToolName
import yaml

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from tools.docker.Docker import Docker
from tools.utils.Log import Log
from tools.utils.parsers import obj_to_jsonstr

RawResult = Any

class Tool(ABC):

    tool_name: ToolName
    image_config_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "docker/image-config"))
    tool_cfg = {}

    def __init__(
        self
    ) -> None:
        pass

    @classmethod
    def load_default_cfg(cls, tool_name: ToolName) -> None:
        if (cls.tool_cfg != {}):
            return
        tool_config_path = os.path.join(cls.image_config_path, f"{tool_name.value}.yaml")
        with open(tool_config_path, "r") as yaml_file:
            cls.tool_cfg = yaml.safe_load(yaml_file)

    @classmethod
    @abstractmethod
    def parse_raw_result(
        cls,
        raw_result: RawResult,
        duration: float,
        file_name: str,
    ) -> FinalResult:
        pass

    @classmethod
    @abstractmethod
    def parse_error_result(cls, errors: list[ToolError], duration: float, file_name: str) -> FinalResult:
        pass

    @classmethod
    @abstractmethod
    def detect_errors(cls, raw_result_str: str) -> list[ToolError]:
        pass

    @classmethod
    def any_error(cls, errors: list[ToolError]) -> bool:
        return len(errors) > 0

    @classmethod
    def analyze(
        cls,
        file_dir_path: str,
        file_name: str,
        docker_image: str="",
        analyze_cmd: str="",
        options: str=""
    ) -> tuple[FinalResult, RawResult]:
        start = time()
        Tool.load_default_cfg(cls.tool_name)
        if (docker_image == ""):
            docker_image = cls.tool_cfg['docker_image']['default']
        if (analyze_cmd == ""):
            analyze_cmd = cls.tool_cfg['analyze_cmd']
        if (options == ""):
            options = cls.tool_cfg['options']
        (errors, raw_result_str) = Docker.run(docker_image, analyze_cmd, file_name, options, file_dir_path)
        errors += cls.detect_errors(raw_result_str)
        final_result: FinalResult
        raw_result_json: RawResult
        end = time()
        if not cls.any_error(errors):
            raw_result_json = json.loads(raw_result_str)
            final_result = cls.parse_raw_result(raw_result_json, duration=end - start, file_name=file_name)
        else:
            final_result = cls.parse_error_result(errors, duration=end - start, file_name=file_name)
            raw_result_json = final_result

        return (final_result, raw_result_json)

    @classmethod
    def export_result(cls, file_name: str, raw_result: RawResult, final_result: FinalResult) -> None:
        path: str = os.path.dirname(__file__)
        path = os.path.join(path, 'results', cls.tool_name.value)
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path, file_name + ".raw_result.json"), "w") as f:
            try:
                f.write(obj_to_jsonstr(raw_result))
            except Exception as e:
                Log.err(f'Error occured when export raw_result of file {file_name}:\n{raw_result}')
                Log.err(e)
        with open(os.path.join(path, file_name + ".final_result.json"), "w") as f:
            try:
                f.write(obj_to_jsonstr(final_result))
            except Exception as e:
                Log.err(f'Error occured when export final_result of file {file_name}:\n{final_result}')
                Log.err(e)
    