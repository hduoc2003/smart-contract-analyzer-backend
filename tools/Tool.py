from abc import ABC, abstractmethod
import asyncio
import json
import os
from time import time
from types import coroutine
from typing import Any, Callable
from tools.type import FinalResult, ToolError, ToolName
import yaml

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from tools.docker.Docker import Docker
from tools.utils.Async import Async
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
        print (docker_image +' ' +  analyze_cmd + ' ' +  options + ' ' + raw_result_str)
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
    async def analyze_async(
        cls,
        file_dir_path: str,
        file_name: str,
        docker_image: str="",
        analyze_cmd: str="",
        options: str=""
    ) -> tuple[FinalResult, RawResult]:
        return cls.analyze(file_dir_path, file_name, docker_image, analyze_cmd, options)

    @classmethod
    def run_tools_async(
        cls,
        file_dir_path: str,
        file_name: str,
        tools: list[ToolName] = [ToolName.Slither]
    ) -> FinalResult:
        """Analyze single file by running multiple tools asynchronously

        Args:
            file_dir_path (str): dir to folder which contains files
            file_name (str): name of the file
            tools (list[ToolName], optional): name of tools used to analyze. Defaults to [ToolName.Mythril].

        Returns:
            FinalResult: merged result of all tools
        """
        Log.info(f"Analyzing {file_name} ..................")
        from tools.Mythril import Mythril
        from tools.Slither import Slither
        tasks: list[Callable] = []
        arr_args: list[list] = []
        for tool_name in tools:
            match tool_name:
                case ToolName.Mythril:
                    tasks.append(Mythril.analyze)
                case ToolName.Slither:
                    tasks.append(Slither.analyze)
                case _:
                    Log.warn(f'Tool.run_tools_async: There are no tool named {tool_name}')
            arr_args.append([file_dir_path, file_name])
        if (len(tasks) != len(tools)):
            raise Exception(f"Tool.run_tools_async: the length of tasks is {len(tasks)} \
                            is not equal to the length of tools which is {len(tools)}")

        result: list[FinalResult] = [final for final, raw in Async.run_functions(tasks, arr_args)]
        Log.info(f"Analyzing {file_name} finished ..............")
        return result[0]
        # Log.info(result)

    @classmethod
    async def analyze_files_async(
        cls,
        file_dir_path: str,
        files_names: list[str]
    ) -> list[FinalResult]:
        return Async.run_single_func(
            func=cls.run_tools_async,
            arr_args=[[file_dir_path, file_name] for file_name in files_names]
        )

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


