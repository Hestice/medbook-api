# appointments.py
from flask import Blueprint, request, jsonify
from datetime import datetime
from flaskr.models import db, Appointment
from .utils import get_current_user_from_session, unauthorized_message

bp = Blueprint('appointments', __name__, url_prefix='/api/appointments')

@bp.route('/', methods=['POST'])
def create_appointment():
    user = get_current_user_from_session()
    if not user:
        return unauthorized_message()

    data = request.json
    new_appointment = Appointment(
        id=data['id'],
        patientId=data['patientId'],
        doctorId=data['doctorId'],
        availabilityId=data['availabilityId'],
        date=datetime.strptime(data['date'], '%Y-%m-%d'),
        time=datetime.strptime(data['time'], '%H:%M:%S').time()
    )
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment created'}), 201

@bp.route('/<id>', methods=['PUT'])
def update_appointment(id):
    user = get_current_user_from_session()
    if not user:
        return unauthorized_message()

    data = request.json
    appointment = Appointment.query.get(id)
    if appointment:
        appointment.date = datetime.strptime(data['date'], '%Y-%m-%d')
        appointment.time = datetime.strptime(data['time'], '%H:%M:%S').time()
        db.session.commit()
        return jsonify({'message': 'Appointment updated'}), 200
    return jsonify({'message': 'Appointment not found'}), 404

@bp.route('/<id>', methods=['DELETE'])
def delete_appointment(id):
    user = get_current_user_from_session()
    if not user:
        return unauthorized_message()

    appointment = Appointment.query.get(id)
    if appointment:
        db.session.delete(appointment)
        db.session.commit()
        return jsonify({'message': 'Appointment deleted'}), 204
    return jsonify({'message': 'Appointment not found'}), 404

@bp.route('/', methods=['GET'])
def list_appointments():
    user = get_current_user_from_session()
    if not user:
        return unauthorized_message()

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    appointments = Appointment.query.filter(
        Appointment.date.between(start_date, end_date)
    ).all()
    return jsonify([appointment.serialize() for appointment in appointments]), 200
