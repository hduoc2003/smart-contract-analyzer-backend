import os
import docker
from docker import errors
import requests
import yaml
from tools.type import ErrorClassification, ToolError

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from tools.utils import Log

# sys.path.append()
class Docker:

    client = docker.from_env()
    cfg_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "config.yaml"))
    with open(os.path.abspath(cfg_path), 'r', encoding='utf-8') as ymlfile:
        try:
            cfg = yaml.safe_load(ymlfile)
        except yaml.YAMLError as exc:
            Log.err(exc)

    @classmethod
    def __cfg_containers(cls):
        return cls.cfg["containers"]
    @classmethod
    def __cfg_containers_run(cls):
        return cls.__cfg_containers()["run"]
    @classmethod
    def __cfg_containers_run_volumes(cls):
        return cls.__cfg_containers_run()["volumes"]
    @classmethod
    def __cfg_containers_run_volumes_bind(cls):
        return cls.__cfg_containers_run_volumes()["bind"]
    @classmethod
    def __cfg_containers_run_timeout(cls):
        return cls.__cfg_containers_run()["timeout"]


    @classmethod
    def pull_image(cls, image: str) -> None:
        try:
            Log.info('pulling ' + image + ' image, this may take a while...')
            image = cls.client.images.pull(image) # type: ignore
            Log.info(f'image {image} pulled')

        except errors.APIError as err:
            Log.err('Errors occurred when pulling image ' + image)
            Log.err(err)


    @classmethod
    def run(cls,
            image: str,
            analyze_cmd: str,
            file_name: str,
            tool_options: str,
            file_dir_path: str
        ) -> tuple[list[ToolError], str]:

        errors: list[ToolError] = []
        logs: str = ""
        cmd = f"{analyze_cmd} {cls.__cfg_containers_run_volumes_bind()}/{file_name} {tool_options}"
        container = cls.client.containers.run(
            image=image,
            command=cmd,
            detach=True,
            volumes={
                f"{file_dir_path}": cls.__cfg_containers_run_volumes()
            }
        )
        try:
            container.wait(timeout=cls.__cfg_containers_run_timeout()) # type: ignore
        except requests.exceptions.ConnectionError as e:
            Log.info('#####################')
            errors.append(ToolError(
                error=ErrorClassification.RuntimeOut,
                msg=f"Time out while running image {image} to analyze {file_name}"
            ))
            Log.err(f"Time out while running image {image} to analyze {file_name}")
            Log.print_except(e)
        
        
        # print(container.logs().decode("utf8"))
        logs: str = container.logs().decode("utf8").strip() # type: ignore
        # Log.info(logs)
        container.remove() # type: ignore
        return (errors, logs)