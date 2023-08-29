from typing import Any, Type
from mongoengine import Document

def update_one(doc: Type[Document], data: dict, **query) -> int:
    """return the number of updated successfully document

    Args:
        doc (Type[Document]): class that extends Document
        data (dict): new value of fields need to updated

    Returns:
        int: _description_
    """
    return doc.objects(**query).update_one(**{"set__" + key: value for key, value in data.items()})