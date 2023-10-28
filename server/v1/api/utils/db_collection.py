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

def get_document_by_id(doc: Type[Document], id: str) -> Type[Document] | None:
    return doc.objects(id = id).first()

def get_some_field_by_id(doc: Type[Document], id: str, fields: list[str]) -> Any:
    return doc.objects(id=id).only(*fields).first()
