import os

def get_contracts_storage_path(username: str, submit_id: str) -> str:
    from server.v1.config.app_config import tool_storage_path
    return os.path.join(tool_storage_path, username, submit_id, "contracts")

def get_all_files(path: str, exts: list[str] = [".sol"]) -> list[str]:
    files: list[str] = []
    if os.path.exists(path) and os.path.isdir(path):
        items: list[str] = os.listdir(path)
        for item in items:
            if os.path.isfile(os.path.join(path, item)):
                name, ext = os.path.splitext(item)
                if ext in exts:
                    files.append(item)
    return files
