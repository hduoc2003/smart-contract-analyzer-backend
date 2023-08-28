from enum import Enum
from mongoengine import Document, StringField, BooleanField, DateTimeField, EnumField
from datetime import datetime

from server.v1.api.utils.FlaskLog import FlaskLog

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

    meta = {
        'collection': 'users'
    }

    @classmethod
    def username_exists(cls, username: str) -> bool:
        return len(cls.objects(username=username)) > 0


    # def __init__(
    #     self,
    #     id: str,
    #     name: str,
    #     username: str,
    #     password: str,
    #     email: str,
    #     role: str,
    #     last_online: datetime | None = None,
    #     email_verified: bool = False,
    #     created_at: datetime | None = None,
    #     last_modified_at: datetime | None = None,
    #     *args, **kwargs
    # ) -> None:
    #     super(UserDoc, self).__init__(*args, **kwargs)
    #     cur_time: datetime = datetime.utcnow()
    #     if (not last_online):
    #         last_online = cur_time
    #     if (not created_at):
    #         created_at = cur_time
    #     if (not last_modified_at):
    #         last_modified_at = cur_time
    #     if (role == "user"):
    #         _role: UserRole = UserRole.USER
    #     else:
    #         if (role == "admin"):
    #             _role = UserRole.ADMIN
    #         else:
    #             # FlaskLog.info(role)
    #             raise Exception(f"Has no role {role} for User")
    #             # _role = UserRole.USER'
    #     FlaskLog.info(args)
    #     FlaskLog.info(kwargs)
    #     self.id=id,
    #     self.name=name,
    #     self.username=username,
    #     self.password=password,
    #     self.email=email,
    #     self.role = _role
    #     self.last_online=last_online,
    #     self.email_verified=email_verified,
    #     self.created_at=created_at,
    #     self.last_modified_at=last_modified_at



