from flask import Blueprint, request, jsonify
from datetime import datetime
from flaskr.models import db, Comment
from .utils import get_current_user_from_session, unauthorized_message

bp = Blueprint('comments', __name__, url_prefix='/api/comments')

@bp.route('/', methods=['POST'])
def create_comment():
    user = get_current_user_from_session()
    if not user:
        return unauthorized_message()

    data = request.json
    new_comment = Comment(
        id=data['id'],
        appointmentId=data['appointmentId'],
        userId=data['userId'],
        content=data['content'],
        createdAt=datetime.utcnow()
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({'message': 'Comment created'}), 201

@bp.route('/<id>', methods=['PUT'])
def update_comment(id):
    user = get_current_user_from_session()
    if not user:
        return unauthorized_message()

    data = request.json
    comment = Comment.query.get(id)
    if comment:
        comment.content = data['content']
        db.session.commit()
        return jsonify({'message': 'Comment updated'}), 200
    return jsonify({'message': 'Comment not found'}), 404

@bp.route('/<id>', methods=['DELETE'])
def delete_comment(id):
    user = get_current_user_from_session()
    if not user:
        return unauthorized_message()

    comment = Comment.query.get(id)
    if comment:
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'message': 'Comment deleted'}), 204
    return jsonify({'message': 'Comment not found'}), 404

@bp.route('/', methods=['GET'])
def list_comments():
    user = get_current_user_from_session()
    if not user:
        return unauthorized_message()

    appointment_id = request.args.get('appointment_id')
    comments = Comment.query.filter_by(appointmentId=appointment_id).all()
    return jsonify([comment.serialize() for comment in comments]), 200
