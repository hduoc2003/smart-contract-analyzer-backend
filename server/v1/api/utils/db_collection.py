from typing import Any, Type, TypeVar
from mongoengine import Document
import json as JSON
from server.v1.api.utils.FlaskLog import FlaskLog
from server.v1.api.utils.dict_utils import exclude_fields, include_fields

T = TypeVar('T', bound=Document)

def update_one(doc: Type[T], data: dict, **query) -> int:
    """return the number of updated successfully document

    Args:
        doc (Type[T]): class that extends Document
        data (dict): new value of fields need to updated

    Returns:
        int: _description_
    """
    return doc.objects(**query).update_one(**{"set__" + key: value for key, value in data.items()})

def get_document(doc: Type[T], id: str) -> T | None:
    return doc.objects(id = id).first()

def get_document_includes(
    doc: Type[T],
    id: str,
    included_fields: list[str],
    json: bool = False
) -> T | dict[str, Any] | None:
    res: T = doc.objects(id=id).only(*included_fields).first()
    if res is None:
        return None
    if not json:
        return res
    return include_fields(document_to_dict(res), included_fields)

def get_document_excludes(
    doc: Type[T],
    id: str,
    excluded_fields: list[str],
    json: bool = False
) -> dict[str, Any] | T | None:
    res: T =  doc.objects(id=id).exclude(*excluded_fields).first()
    if res is None:
        return None
    if not json:
        return res
    return exclude_fields(document_to_dict(res), excluded_fields)

def document_to_dict(doc: T) -> dict[str, Any]: # type:ignore
    return doc.to_mongo().to_dict()
