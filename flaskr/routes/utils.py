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

def paginate(query, page, per_page):
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    return {
        'total': total,
        'page': page,
        'per_page': per_page,
        'items': items
    }