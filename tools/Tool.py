from abc import ABC, abstractmethod
import json
import os
import re
import time
from typing import Any, Callable, Generator
from tools.types import AnalysisIssue, AnalysisResult, ErrorClassification, FinalResult, ImageConfig, ImageVolume, ToolAnalyzeArgs, ToolError, ToolName
import yaml
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from tools.utils.Async import Async
from tools.utils.Log import Log
from tools.utils.parsers import obj_to_jsonstr
from tools.utils.merge_tools import DuplicateIssue

RawResult = Any

class Tool(ABC):

    tool_name: ToolName
    image_config_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "docker/image-config"))
    storage_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "storage"))
    tool_cfg: ImageConfig

    valid_solcs: list[str] = ['0.8.21', '0.8.20', '0.8.19', '0.8.18', '0.8.17', '0.8.16', '0.8.15', '0.8.14', '0.8.13', '0.8.12', '0.8.11', '0.8.10', '0.8.9', '0.8.8', '0.8.7', '0.8.6', '0.8.5', '0.8.4', '0.8.3', '0.8.2', '0.8.1', '0.8.0', '0.7.6', '0.7.5', '0.7.4', '0.7.3', '0.7.2', '0.7.1', '0.7.0', '0.6.12', '0.6.11', '0.6.10', '0.6.9', '0.6.8', '0.6.7', '0.6.6', '0.6.5', '0.6.4', '0.6.3', '0.6.2', '0.6.1', '0.6.0', '0.5.17', '0.5.16', '0.5.15', '0.5.14', '0.5.13', '0.5.12', '0.5.11', '0.5.10', '0.5.9', '0.5.8', '0.5.7', '0.5.6', '0.5.5', '0.5.4', '0.5.3', '0.5.2', '0.5.1', '0.5.0', '0.4.26', '0.4.25', '0.4.24', '0.4.23', '0.4.22', '0.4.21', '0.4.20', '0.4.19', '0.4.18', '0.4.17', '0.4.16', '0.4.15', '0.4.14', '0.4.13', '0.4.12', '0.4.11', '0.4.10', '0.4.9', '0.4.8', '0.4.7', '0.4.6', '0.4.5', '0.4.3', '0.4.2', '0.4.1', '0.4.0']
    valid_solcs_str = ",".join(valid_solcs)

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
        solc: str
    ) -> FinalResult:
        pass

    @classmethod
    @abstractmethod
    def parse_error_result(
        cls,
        errors: list[ToolError],
        duration: float,
        file_name: str,
        solc: str
    ) -> FinalResult:
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
        args: ToolAnalyzeArgs
    ) -> tuple[list[ToolError], str]:
        pass

    @classmethod
    def analyze(
        cls,
        args: ToolAnalyzeArgs
    ) -> tuple[FinalResult, RawResult]:
        # Log.info(f'Running {cls.tool_name.value}')
        start = time.time()
        solc: str | ErrorClassification = args.solc or Tool.get_solc_version(args.sub_container_file_path, args.file_name)
        if (isinstance(solc, ErrorClassification)):
            raise Exception(f"Tool:analyze: {solc}")
        (errors, raw_result_str) = cls.run_core(ToolAnalyzeArgs(
            sub_container_file_path=args.sub_container_file_path,
            file_name=args.file_name,
            solc=solc, # type: ignore
            docker_image=args.docker_image or cls.tool_cfg.docker_image,
            options=args.options or cls.tool_cfg.options,
            timeout=args.timeout if args.timeout > -1 else cls.tool_cfg.timeout
        ))
        errors += cls.detect_errors(raw_result_str)
        final_result: FinalResult
        raw_result_json: RawResult
        end = time.time()
        if not cls.any_error(errors):
            raw_result_json = json.loads(raw_result_str)
            final_result = cls.parse_raw_result(raw_result_json, duration=end - start, file_name=args.file_name, solc=solc) # type: ignore
        else:
            final_result = cls.parse_error_result(errors, duration=end - start, file_name=args.file_name, solc=solc) #type: ignore
            raw_result_json = final_result

        return (final_result, raw_result_json)

    @staticmethod
    def merge_results(results: list[FinalResult], duration: float) -> FinalResult:
        if len(results) == 1:
            return results[0]

        file_name: str = results[0].file_name
        tool_name: str = "Mythril, Slither"
        solc: str = results[0].solc
        analysisResult: AnalysisResult = DuplicateIssue.merge(results[0], results[1])
        return FinalResult(
            file_name=file_name,
            tool_name=tool_name,
            duration=duration,
            solc=solc,
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
        solc: str = results[0].solc
        errors: list[ToolError] = results[0].analysis.errors
        issues: list[AnalysisIssue] = results[0].analysis.issues
        solc: str = results[0].solc

        for i in range(1, len(results)):
            tool_name += f", {results[i].tool_name}"
            errors += results[i].analysis.errors
            issues += results[i].analysis.issues
        return FinalResult(
            file_name=file_name,
            tool_name=tool_name,
            duration=duration,
            solc= solc,
            analysis=AnalysisResult(
                errors=errors,
                issues=issues
            )
        )

    @classmethod
    def get_tool_error(cls, error: ErrorClassification, **kwargs) -> ToolError:
        match error:
            case ErrorClassification.RuntimeOut:
                return ToolError(
                    error=error,
                    msg=f"Run timeout"
                )
            case ErrorClassification.CompileError:
                return ToolError(
                    error=error,
                    msg=kwargs['msg']
                )
            case ErrorClassification.UnsupportedSolc:
                return ToolError(
                    error=error,
                    msg=f"We only support Solidity from version {cls.valid_solcs[-1]} to {cls.valid_solcs[0]}, please use another Solidity version in source code."
                )
            case ErrorClassification.UndefinedSolc:
                return ToolError(
                    error=error,
                    msg=f"The solidity version you declared does not exist, please check again."
                )
            case ErrorClassification.UnknownError:
                return ToolError(
                    error=error,
                    msg=f"Unknown error"
                )
            case _:
                raise Exception(f"Tool.get_tool_error: {error} is not processed yet.")


    @classmethod
    def analyze_single_file(cls, args: ToolAnalyzeArgs,tools: list[ToolName] = [ToolName.Mythril, ToolName.Slither]) -> FinalResult:
            start: float = time.time()
            from tools.Mythril import Mythril
            from tools.Slither import Slither
            solc: str | ErrorClassification = args.solc or cls.get_solc_version(args.sub_container_file_path, args.file_name)
            if (isinstance(solc, ErrorClassification)):
                return FinalResult(
                    file_name=args.file_name,
                    tool_name="",
                    duration=time.time() - start,
                    solc="",
                    analysis=AnalysisResult(
                        errors=[cls.get_tool_error(solc)],
                        issues=[]
                    )
                )
            Log.info(f"Analyzing {args.file_name} using solc {solc} ..................")
            tasks: list[Callable] = []
            arr_args: list[list] = []
            for tool_name in tools:
                match tool_name:
                    case ToolName.Mythril:
                        tasks.append(Mythril.analyze)
                    case ToolName.Slither:
                        tasks.append(Slither.analyze)
                    case _:
                        Log.warn(f'Function analyze_single_file: There are no tool named {tool_name}')
                arr_args.append([ToolAnalyzeArgs(
                    sub_container_file_path=args.sub_container_file_path,
                    file_name=args.file_name,
                    solc=solc
                )])
            if (len(tasks) != len(tools)):
                raise Exception(f"Function analyze_single_file: the length of tasks is {len(tasks)} \
                                is not equal to the length of tools which is {len(tools)}")

            results: list[FinalResult] = [final for final, raw in Async.run_functions(tasks, arr_args)]
            Log.info(f"Analyzing {args.file_name} finished ..............")
            end:float = time.time()
            # print(results)

            return cls.merge_results(results, duration=end-start)
    @classmethod
    def analyze_files_async(
        cls,
        files: list[ToolAnalyzeArgs],
        tools: list[ToolName] = [ToolName.Mythril, ToolName.Slither],
        stream: bool = False
    ) -> Generator | list[FinalResult]:

        def analyze_single_file(args: ToolAnalyzeArgs) -> FinalResult:
            start: float = time.time()
            from tools.Mythril import Mythril
            from tools.Slither import Slither
            solc: str | ErrorClassification = args.solc or cls.get_solc_version(args.sub_container_file_path, args.file_name)
            if (isinstance(solc, ErrorClassification)):
                return FinalResult(
                    file_name=args.file_name,
                    tool_name="",
                    duration=time.time() - start,
                    solc="",
                    analysis=AnalysisResult(
                        errors=[cls.get_tool_error(solc)],
                        issues=[]
                    )
                )
            Log.info(f"Analyzing {args.file_name} using solc {solc} ..................")
            tasks: list[Callable] = []
            arr_args: list[list] = []
            for tool_name in tools:
                match tool_name:
                    case ToolName.Mythril:
                        tasks.append(Mythril.analyze)
                    case ToolName.Slither:
                        tasks.append(Slither.analyze)
                    case _:
                        Log.warn(f'Function analyze_single_file: There are no tool named {tool_name}')
                arr_args.append([ToolAnalyzeArgs(
                    sub_container_file_path=args.sub_container_file_path,
                    file_name=args.file_name,
                    solc=solc
                )])
            if (len(tasks) != len(tools)):
                raise Exception(f"Function analyze_single_file: the length of tasks is {len(tasks)} \
                                is not equal to the length of tools which is {len(tools)}")

            results: list[FinalResult] = [final for final, raw in Async.run_functions(tasks, arr_args)]
            Log.info(f"Analyzing {args.file_name} finished ..............")
            end:float = time.time()
            # print(results)

            return cls.merge_results(results, duration=end-start)
            # return results[0]

        if (stream):
            return Async.run_single_func_stream(
                func=analyze_single_file,
                arr_args=[[file] for file in files]
            )

        return Async.run_single_func(
                func=analyze_single_file,
                arr_args=[[file] for file in files]
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

    #NOTE: For testing
    @classmethod
    def export_merge_result(cls, file_name: str, result, duration, directory_path):
        split_parts = file_name.split("-")
        swc_number = ''.join(filter(str.isdigit, split_parts[1]))
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
        directory_path = os.path.join("tools","utils", "duplicate_issues", f"swc-{swc_number}", f"{os.path.splitext(file_name)[0]}")
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

    @classmethod
    def get_solc_version(
        cls,
        sub_container_file_path: str,
        file_name: str
    ) -> str | ErrorClassification:
        """Xác định phiên bản solidity được khai báo trong mã nguồn

        Args:
            sub_container_file_path (str): _description_
            file_name (str): _description_

        Returns:
            str | int: -1 Nếu không thể xác định được phiên bản
                        0 Nếu phiên bản xác định được không được hỗ trợ
        """
        file_path = os.path.join(cls.storage_path, sub_container_file_path, file_name)
        solc: str = ""
        with open(file_path, "r") as file:
            source_code: str = file.read()

            # Loại bỏ khối comment
            source_code = re.sub(r"/\*.*?\*/", "", source_code, flags=re.DOTALL)
            lines: list[str] = source_code.splitlines()
            for line in lines:
                line: str = line.split(r"//")[0]
                match: re.Match[str] | None = re.search(r"pragma\s+solidity\s+([<>=^]*[\d]+\.[\d]+(\.[\d]+)?)", line)
                if match:
                    solc = match.group(1)
                    if (solc.count('.') == 1):
                        solc += '.0'
                    break
            if (solc == ""):
                return ErrorClassification.UndefinedSolc
            res: str = ""
            match solc[0]:
                case '^':
                    res = solc[1:]
                    if (res not in cls.valid_solcs):
                        return ErrorClassification.UnsupportedSolc
                case '>':
                    if (solc[1] == '='):
                        res = solc[2:]
                    else:
                        try:
                            i: int = cls.valid_solcs.index(solc[1:])
                            if (i == 0):
                                return ErrorClassification.UnsupportedSolc
                            res = cls.valid_solcs[i-1]
                        except ValueError:
                            return ErrorClassification.UnsupportedSolc
                case '<':
                    if (solc[1] == '='):
                        res = solc[2:]
                    else:
                        try:
                            i: int = cls.valid_solcs.index(solc[1:])
                            if (i == len(cls.valid_solcs) - 1):
                                return ErrorClassification.UnsupportedSolc
                            res = cls.valid_solcs[i+1]
                        except ValueError:
                            return ErrorClassification.UnsupportedSolc
                case _:
                    return solc if solc in cls.valid_solcs else ErrorClassification.UndefinedSolc

            return res if res[0].isdigit() else ErrorClassification.UndefinedSolc
