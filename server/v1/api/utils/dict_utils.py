from typing import Any


def include_fields(data: dict[str, Any], fields: list[str]) -> dict[str, Any]:
    """lấy tất cả các field trong mảng fields từ data

    Args:
        data (dict[str, Any]): _description_
        fields (list[str]): _description_

    Returns:
        dict[str, Any]: _description_
    """
    return {
        key: data[key] for key in fields if key in data
    }

def exclude_fields(data: dict[str, Any], fields: list[str]) -> dict[str, Any]:
    """loại tất cả các field

    Args:
        data (dict[str, Any]): _description_
        fields (list[str]): _description_

    Returns:
        dict[str, Any]: _description_
    """
    return {
        key: data[key] for key in data.keys() if key not in fields
    }
