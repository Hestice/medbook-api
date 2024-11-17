from flask import Blueprint, request, jsonify
from datetime import datetime, time
from flaskr.models import db, Availability
from .utils import get_current_user_from_session, unauthorized_message

bp = Blueprint('availabilities', __name__, url_prefix='/api/availabilities')

@bp.route('/', methods=['POST'])
def create_availability():
    user = get_current_user_from_session()
    if not user:
        return unauthorized_message()

    data = request.json
    if isinstance(data, list): 
        for item in data:
            if isinstance(item, dict):
                doctor_id = item.get('doctorId')
                available_from = item.get('availableFrom')
                available_to = item.get('availableTo')

                if doctor_id and available_from and available_to:
                    new_availability = Availability(
                        doctorId=doctor_id,
                        availableFrom=datetime.strptime(available_from, '%Y-%m-%d %H:%M:%S'),
                        availableTo=datetime.strptime(available_to, '%Y-%m-%d %H:%M:%S')
                    )
                    db.session.add(new_availability)
            else:
                return jsonify({'message': 'Invalid data format'}), 400
        
        db.session.commit()
        return jsonify({'message': 'Availabilities created'}), 201

    return jsonify({'message': 'Expected an array of availabilities'}), 400


@bp.route('/<id>', methods=['PUT'])
def update_availability(id):
    user = get_current_user_from_session()
    if not user or user.role != 'doctor':
        return unauthorized_message()

    data = request.json
    availability = Availability.query.get(id)
    if availability:
        availability.doctorId = data['doctorId']
        availability.availableFrom = datetime.strptime(data['start'], '%H:%M:%S').time()
        availability.availableTo = datetime.strptime(data['end'], '%H:%M:%S').time()
        db.session.commit()
        return jsonify({'message': 'Availability updated'}), 200
    return jsonify({'message': 'Availability not found'}), 404

@bp.route('/<id>', methods=['DELETE'])
def delete_availability(id):
    user = get_current_user_from_session()
    if not user or user.role != 'doctor':
        return unauthorized_message()

    availability = Availability.query.get(id)
    if availability:
        db.session.delete(availability)
        db.session.commit()
        return jsonify({'message': 'Availability deleted'}), 204
    return jsonify({'message': 'Availability not found'}), 404

@bp.route('/', methods=['GET'])
def list_availabilities():
    user = get_current_user_from_session()
    if not user or user.role != 'doctor':
        return unauthorized_message()

    availabilities = Availability.query.filter_by(doctorId=user.uuid).all()
    return jsonify([availability.serialize() for availability in availabilities]), 200
