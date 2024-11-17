from flask import jsonify, session
from flaskr.models import User

def get_current_user_from_session():
    user_uuid = session.get('user_uuid')
    if user_uuid:
        user = User.query.filter_by(uuid=user_uuid).first()
        if user:
            return user
    return None
def unauthorized_message():
    return jsonify({"error": "Unauthorized, please login first"}), 401
