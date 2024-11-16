from flask import Blueprint, request, jsonify
from flaskr.models import db, Availability
from datetime import datetime

bp = Blueprint('availabilities', __name__, url_prefix='api/availabilities')

@bp.route('/', methods=['POST'])
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
def delete_availability(id):
    availability = Availability.query.get(id)
    if availability:
        db.session.delete(availability)
        db.session.commit()
        return jsonify({'message': 'Availability deleted'}), 204
    return jsonify({'message': 'Availability not found'}), 404

@bp.route('/', methods=['GET'])
def list_availabilities():
    availabilities = Availability.query.all()
    return jsonify([availability.serialize() for availability in availabilities]), 200
