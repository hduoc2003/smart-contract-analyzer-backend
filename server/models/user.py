from mongoengine import Document, StringField, ReferenceField, ObjectIdField, BooleanField, DateTimeField

from datetime import datetime

class User(Document):
    name: StringField
    username = StringField(required=True) #username is enough
    password = StringField(required=True)
    email = StringField(required=True)
    email_verified = BooleanField(required=True, default=False)
    last_online = DateTimeField()
    created_at = DateTimeField(default=datetime.now())
    last_modified_at = DateTimeField(default=datetime.now())