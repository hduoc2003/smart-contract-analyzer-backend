from datetime import datetime
from server.models.user import User

def update_last_online(username):
    user = User.objects(username=username).first()
    if user:
        user.last_online = datetime.now()
        user.save()

def get_field_value(username, field_name):
    """
    Dùng cái này gán tên người dùng và field cần lấy, đỡ viết nhiều hàm get quá
    Args:
        username (str): tên người dùng
        field_name (str): email, created_at, etc

    Returns:
        Giá trị của field_name
    """    
    #example: user = User.objects(last_online="john123").first()
    user = User.objects(**{field_name: username}).first()    
    if user:
        return getattr(user, field_name)
    return None

# def get_last_online(username):
#     user = User.objects(username=username).first()
#     if user:
#         return user.last_online
#     return None

# def get_create_at(time):
#     user = User.objects(time=time).first()
#     if user:
#         return user.create_at
#     return None
