import os
from server.v1.api.utils.path import get_contracts_storage_path
from werkzeug.datastructures.file_storage import FileStorage


def save_contract(submit_id: str, file_id: str, file_data: FileStorage | str, user_id: str) -> str:
    user_storage: str = get_contracts_storage_path(user_id=user_id, submit_id=submit_id)
    if not os.path.exists(user_storage):
        os.makedirs(user_storage)
    path: str = os.path.join(user_storage, file_id +'.sol')

    if isinstance(file_data, str):
        with open(path, 'w', encoding='utf-8') as writer:
            writer.write(file_data)
            return file_data

    try:
        file_data.save(path)
        with open(path, "r") as source_code:
            return source_code.read()
    except Exception as e:
        print("File not exist")
        return ""
