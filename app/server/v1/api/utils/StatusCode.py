from enum import Enum, unique

@unique
class StatusCode(Enum):
    OK = 200
    BadRequest = 400
    NotFound = 404
    Conflict = 409
    InternalServerError = 500
