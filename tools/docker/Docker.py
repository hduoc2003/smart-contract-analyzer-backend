import os
import docker
from docker import errors
import requests
import yaml
from tools.type import ErrorClassification, ToolError
from tools.utils.Log import Log

# sys.path.append()
class Docker:

    client = docker.from_env()

    @classmethod
    def pull_image(cls, image: str) -> None:
        try:
            Log.info('pulling ' + image + ' image, this may take a while...')
            image = cls.client.images.pull(image) # type: ignore
            Log.info(f'image {image} pulled')

        except errors.APIError as err:
            Log.err('Errors occurred when pulling image ' + image)
            Log.err(err)

    @staticmethod
    def create_volumes(host_paths: list[str], container_paths: list[str]) -> dict[str, dict[str, str]]:
        if (len(host_paths) != len(container_paths)):
            raise Exception(f"Docker.create_volumes: the length of host_paths {len(host_paths)} is not equal to the length of container_paths {len(container_paths)}")
        return {
            host_path: {
                'bind': container_paths[i],
                'mode': 'ro'
            }   for i, host_path in enumerate(host_paths)
        }

