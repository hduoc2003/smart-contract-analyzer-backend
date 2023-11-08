import os

def get_env(key: str) -> str:
    value: str | None = os.getenv(key)
    print(value)
    if (not value):
        raise Exception(f"Enviroment variable with key {key} is not exists")
    return value
