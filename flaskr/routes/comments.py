from flask import Blueprint, request, jsonify
from flaskr.models import db, Comment
from datetime import datetime

bp = Blueprint('comments', __name__, url_prefix='/api/comments')

@bp.route('/', methods=['POST'])
def create_comment():
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
    data = request.json
    comment = Comment.query.get(id)
    if comment:
        comment.content = data['content']
        db.session.commit()
        return jsonify({'message': 'Comment updated'}), 200
    return jsonify({'message': 'Comment not found'}), 404

@bp.route('/<id>', methods=['DELETE'])
def delete_comment(id):
    comment = Comment.query.get(id)
    if comment:
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'message': 'Comment deleted'}), 204
    return jsonify({'message': 'Comment not found'}), 404

@bp.route('/', methods=['GET'])
def list_comments():
    appointment_id = request.args.get('appointment_id')
    comments = Comment.query.filter_by(appointmentId=appointment_id).all()
    return jsonify([comment.serialize() for comment in comments]), 200
