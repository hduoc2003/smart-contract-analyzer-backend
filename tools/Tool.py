from abc import ABC, abstractmethod
import asyncio
import json
import os
import time
from types import coroutine
from typing import Any, Callable, List
from tools.type import AnalysisIssue, AnalysisResult, FinalResult, ImageConfig, ImageVolume, ToolError, ToolName
import yaml

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from tools.docker.Docker import Docker
from tools.utils.Async import Async
from tools.utils.Log import Log
from tools.utils.parsers import obj_to_jsonstr
from tools.utils.mergeTools import DuplicateIssue
RawResult = Any

class Tool(ABC):

    tool_name: ToolName
    image_config_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "docker/image-config"))
    storage_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "storage"))
    tool_cfg: ImageConfig

    def __init__(
        self
    ) -> None:
        pass

    @classmethod
    def load_default_cfg(cls, tool_name: ToolName) -> ImageConfig:
        tool_config_path = os.path.join(cls.image_config_path, f"{tool_name.value}.yaml")
        # print(cls.tool_name)
        with open(tool_config_path, "r") as yaml_file:
            cfg = yaml.safe_load(yaml_file)
            tool_cfg = ImageConfig(
                docker_image=cfg['docker_image'],
                analyze_cmd=cfg['analyze_cmd'],
                options=cfg['options'],
                volumes=ImageVolume(
                    bind=cfg['volumes']['bind'],
                    mode=cfg['volumes']['mode']
                ),
                timeout=cfg['timeout']
            ) # type: ignore
        return tool_cfg

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
    @abstractmethod
    def run_core(
        cls,
        container_file_path: str,
        file_name: str,
        docker_image: str,
        options: str,
        timeout: int = -1
    ) -> tuple[list[ToolError], str]:
        pass

    @classmethod
    def analyze(
        cls,
        sub_container_file_path: str,
        file_name: str,
        docker_image: str="",
        options: str="",
        timeout: int = -1
    ) -> tuple[FinalResult, RawResult]:
        Log.info(f'Running {cls.tool_name.value}')
        start = time.time()
        container_file_path = f"{cls.tool_cfg.volumes.bind}/{sub_container_file_path}"
        (errors, raw_result_str) = cls.run_core(
            container_file_path,
            file_name,
            docker_image or cls.tool_cfg.docker_image,
            options or cls.tool_cfg.options,
            timeout if timeout > -1 else cls.tool_cfg.timeout
        )
        errors += cls.detect_errors(raw_result_str)
        final_result: FinalResult
        raw_result_json: RawResult
        end = time.time()
        if not cls.any_error(errors):
            raw_result_json = json.loads(raw_result_str)
            final_result = cls.parse_raw_result(raw_result_json, duration=end - start, file_name=file_name)
        else:
            final_result = cls.parse_error_result(errors, duration=end - start, file_name=file_name)
            raw_result_json = final_result

        return (final_result, raw_result_json)

    @staticmethod
    def merge_results(results: list[FinalResult], duration: float) -> FinalResult:
        
        file_name: str = results[0].file_name
        tool_name: str = results[0].tool_name
        analysisResult: AnalysisResult = DuplicateIssue.merge(results[0], results[1])
        return FinalResult(
            file_name=file_name,
            tool_name=tool_name, #co van de 
            duration=duration,
            analysis=AnalysisResult(
                errors=analysisResult.errors,
                issues=analysisResult.issues
            )
        )
        
    #Giữ lại để đối chiếu với kết quả sau merge thật, TODO: xong merge tool thì xoá
    @staticmethod
    def merge_results_raw(results: list[FinalResult], duration: float) -> FinalResult:
        file_name: str = results[0].file_name
        tool_name: str = results[0].tool_name
        errors: list[ToolError] = results[0].analysis.errors
        issues: list[AnalysisIssue] = results[0].analysis.issues
        for i in range(1, len(results)):
            tool_name += f", {results[i].tool_name}"
            errors += results[i].analysis.errors
            issues += results[i].analysis.issues
        return FinalResult(
            file_name=file_name,
            tool_name=tool_name,
            duration=duration,
            analysis=AnalysisResult(
                errors=errors,
                issues=issues
            )
        )
    @classmethod
    def run_tools_async(
        cls,
        sub_container_file_path: str,
        file_name: str,
        tools: list[ToolName] = [ToolName.Mythril, ToolName.Slither]
    ) -> FinalResult:
        """Analyze single file by running multiple tools asynchronously

        Args:
            sub_container_file_path (str): sub dir to folder which contains files (from storage folder)
            file_name (str): name of the file
            tools (list[ToolName], optional): name of tools used to analyze. Defaults to [ToolName.Mythril].

        Returns:
            FinalResult: merged result of all tools
        """
        start = time.time()
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
            arr_args.append([sub_container_file_path, file_name])
        if (len(tasks) != len(tools)):
            raise Exception(f"Tool.run_tools_async: the length of tasks is {len(tasks)} \
                            is not equal to the length of tools which is {len(tools)}")

        results: list[FinalResult] = [final for final, raw in Async.run_functions(tasks, arr_args)]
        Log.info(f"Analyzing {file_name} finished ..............")
        end = time.time()

        #chỉ dùng để check TODO: Xong thì xoá
        cls.export_merge_result(file_name, cls.merge_results(results, duration=end-start), duration= end-start)
        cls.export_raw_result(file_name, cls.merge_results_raw(results, duration=end-start), duration= end-start)
        
        return cls.merge_results(results, duration=end-start)
        # Log.info(result)

    @classmethod
    def analyze_files_async(
        cls,
        sub_container_file_path: str,
        files_names: list[str],
        tools: list[ToolName] = [ToolName.Mythril, ToolName.Slither]
    ) -> list[FinalResult]:
        return Async.run_single_func(
            func=cls.run_tools_async,
            arr_args=[[sub_container_file_path, file_name, tools] for file_name in files_names],
        )

    @classmethod
    def export_result(cls, file_name: str, raw_result: RawResult, final_result: FinalResult, path: str) -> None:
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
    
    @classmethod
    def export_merge_result(cls, file_name: str, result, duration):
        split_parts = file_name.split("-")
        swc_number = ''.join(filter(str.isdigit, split_parts[1]))
        directory_path = os.path.join("BE","tools","utils", "duplicateIssue", f"swc-{swc_number}", f"{os.path.splitext(file_name)[0]}")
        os.makedirs(directory_path, exist_ok=True)  # Create directories if they don't exist
        try: 
            if isinstance(result, FinalResult):
                file_name1 = os.path.splitext(file_name)[0] + '-merged-result.json'
                file_path1 = os.path.join(directory_path, file_name1)
                with open(file_path1, 'w') as json_file:
                    json_file.write(obj_to_jsonstr(result))
                Log.info("Export merge successful" )
        except Exception as e:
            Log.err(f'Error occured when export raw_result of file {os.path.join(directory_path, file_name)}')
            Log.err(e)
         
    @classmethod
    def export_raw_result(cls, file_name: str, result, duration):
        split_parts = file_name.split("-")
        swc_number = ''.join(filter(str.isdigit, split_parts[1]))

        print("SWC_NUMBER", swc_number)
        directory_path = os.path.join("BE","tools","utils", "duplicateIssue", f"swc-{swc_number}", f"{os.path.splitext(file_name)[0]}")
        os.makedirs(directory_path, exist_ok=True)  # Create directories if they don't exist
        try:
            if isinstance(result, FinalResult):
                file_name1 = os.path.splitext(file_name)[0] + '-raw-result.json'
                file_path1 = os.path.join(directory_path, file_name1)
                with open(file_path1, 'w') as json_file:
                    json_file.write(obj_to_jsonstr(result))
                Log.info("Export raw successful")

        except Exception as e:
            Log.err(f'Error occured when export raw_result of file {os.path.join(directory_path, file_name)}')
            Log.err(e)
        
    