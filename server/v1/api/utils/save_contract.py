import os
from server.v1.api.utils.path import get_contracts_storage_path
from werkzeug.datastructures.file_storage import FileStorage


def save_file(id: str, file_id: str, file_data: FileStorage, user_name: str) -> str:
    try:
        user_storage: str = get_contracts_storage_path(username=user_name, submit_id=id)
        if not os.path.exists(user_storage):
            os.makedirs(user_storage)
        path: str = os.path.join(user_storage, file_id +'.sol')
        file_data.save(path)
        with open(path, "r") as source_code:
            return source_code.read()
    except Exception as e:
        print("File not exist")
        return ""
