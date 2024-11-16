from flask import Blueprint, request, jsonify
from flask_login import login_required
from flaskr.models import db, Availability
from datetime import datetime

bp = Blueprint('availabilities', __name__, url_prefix='/api/availabilities')

@bp.route('/', methods=['POST'])
@login_required
def create_availability():
    data = request.json
    new_availability = Availability(
        id=data['id'],
        doctorId=data['doctorId'],
        availableFrom=datetime.strptime(data['availableFrom'], '%Y-%m-%d %H:%M:%S'),
        availableTo=datetime.strptime(data['availableTo'], '%Y-%m-%d %H:%M:%S')
    )
    db.session.add(new_availability)
    db.session.commit()
    return jsonify({'message': 'Availability created'}), 201

@bp.route('/<id>', methods=['PUT'])
@login_required
def update_availability(id):
    data = request.json
    availability = Availability.query.get(id)
    if availability:
        availability.availableFrom = datetime.strptime(data['availableFrom'], '%Y-%m-%d %H:%M:%S')
        availability.availableTo = datetime.strptime(data['availableTo'], '%Y-%m-%d %H:%M:%S')
        db.session.commit()
        return jsonify({'message': 'Availability updated'}), 200
    return jsonify({'message': 'Availability not found'}), 404

@bp.route('/<id>', methods=['DELETE'])
@login_required
def delete_availability(id):
    availability = Availability.query.get(id)
    if availability:
        db.session.delete(availability)
        db.session.commit()
        return jsonify({'message': 'Availability deleted'}), 204
    return jsonify({'message': 'Availability not found'}), 404

@bp.route('/', methods=['GET'])
@login_required
def list_availabilities():
    availabilities = Availability.query.all()
    return jsonify([availability.serialize() for availability in availabilities]), 200
