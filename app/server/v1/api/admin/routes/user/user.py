from flask import Blueprint, Response, request, jsonify
from server.v1.api.client.models.user_collection import UserDoc
from server.v1.api.utils.db_collection import update_one
from server.v1.api.utils.FlaskLog import FlaskLog
from server.v1.api.utils.StatusCode import StatusCode

user_route = Blueprint("user", __name__, url_prefix="/user")

@user_route.route("/", methods=["GET"])
def get_all_users() -> Response | tuple[str, int]:
    try:
        result = UserDoc.objects.all()
        data = [item for item in result]
        return jsonify(data)
    except Exception as e:
        return str(e), StatusCode.InternalServerError.value


@user_route.route("/<string:user_id>", methods=["GET"])
def search_user(user_id) -> Response | tuple[Response, int]:
    try:
        user = UserDoc.objects(id=user_id).first()

        if user:
            # user['_id'] = str(user['_id'])
            return jsonify(user)
        else:
            return jsonify({'message': 'User not found', 'user_id': user_id}), StatusCode.NotFound.value
    except Exception as e:
        return jsonify({'message': str(e)}), StatusCode.InternalServerError.value


@user_route.route('/delete/<string:user_id>', methods=["DELETE"])
def delete_user(user_id) -> tuple[Response, int]:
    try:
        delete_user = UserDoc.objects(id=user_id).delete()

        if delete_user:
            return jsonify({'message': f'User {user_id} deleted successfully'}), StatusCode.OK.value
        else:
            return jsonify({'message': 'User not found'}), StatusCode.NotFound.value
    except Exception as e:
        return jsonify({'message': str(e)}), StatusCode.InternalServerError.value


@user_route.route('/update/<string:user_id>', methods=["PUT"])
def update_user(user_id) -> tuple[Response, int]:
    try:
        updated_data = request.get_json()
        user_updated: int = update_one(UserDoc, updated_data, id=user_id)
        if (user_updated > 0):
            return jsonify({'message': 'User updated successfully'}), StatusCode.OK.value
        # else:
        return jsonify({'message': 'User not found'}), StatusCode.NotFound.value # user_updated = 0 => user not found

    except Exception as e:
        return jsonify({'message': str(e)}), StatusCode.InternalServerError.value
