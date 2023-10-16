from enum import Enum
from typing import Any
from mongoengine import Document, StringField, BooleanField, DateTimeField, EnumField
from datetime import datetime
import uuid


class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"

class UserDoc(Document):
    id = StringField(required=True, primary_key=True)
    name = StringField(required=True)
    username = StringField(required=True)
    password = StringField(required=True)
    role = EnumField(UserRole, required=True)
    email = StringField(required=True)
    email_verified = BooleanField(required=True, default=False)
    last_online = DateTimeField(default=datetime.utcnow())
    created_at = DateTimeField(default=datetime.utcnow())
    last_modified_at = DateTimeField(default=datetime.utcnow())

    meta: dict[str, str] = {
        'collection': 'users'
    }

def username_exists(username: str) -> bool:
    user = UserDoc.objects(username=username).first()

    # If a user with the given username is found, return True; otherwise, return False
    return user is not None

def update_last_online(username) -> None:

    user = UserDoc.objects(username=username).first()
        # uk_users = User.objects(country='uk')
    if user:
        user.last_online = datetime.now()
        user.save()

def get_field_value(username, field_name) -> Any | None:
    """
    Dùng cái này gán tên người dùng và field cần lấy, đỡ viết nhiều hàm get quá
    Args:
        username (str): tên người dùng
        field_name (str): email, created_at, etc

    Returns:
        Giá trị của field_name
    """
    #example: user = User.objects(last_online="john123").first()
    user = UserDoc.objects(**{field_name: username}).first()
    if user:
        return getattr(user, field_name)
    return None

def create_new_user(data: Any, username: str):
    current_time: datetime = datetime.utcnow()
    new_user = UserDoc(
        id=str(uuid.uuid4()),
        name=data.get('name'),
        username=username,
        password=data.get('password'),
        email=data.get('email'),
        role=data.get("role")
    ).save()
    return new_user

def format_sign_up_response(new_user: UserDoc, username: str, current_time: datetime) -> dict:
    return {
        "message": "Sign Up successful",
        "_id": new_user.id,
        "name": new_user.name,
        "username": username,
        "password": new_user.password,
        "email": new_user.email,
        "email_verified": False,
        "last_online": current_time,
        "created_at": current_time,
        "last_modified_at": current_time  # TODO: Not current time
}

