# appointments.py
from flask import Blueprint, request, jsonify
from datetime import datetime
from flaskr.models import Availability, User, db, Appointment
from .utils import get_current_user_from_session, unauthorized_message

bp = Blueprint('appointments', __name__, url_prefix='/api/appointments')

@bp.route('/', methods=['POST'])
def create_appointment():
    user = get_current_user_from_session()
    if not user:
        return unauthorized_message()

    data = request.json
    
    appointment_from = datetime.strptime(data['from'], '%Y-%m-%d %H:%M:%S')
    appointment_to = datetime.strptime(data['to'], '%Y-%m-%d %H:%M:%S')

    new_appointment = Appointment(
        patientId=data['patientId'],
        doctorId=data['doctorId'],
        availabilityId=data['availabilityId'],
        appointment_from=appointment_from,
        appointment_to=appointment_to,
        patient_name=data['patient_name']
    )

    db.session.add(new_appointment)

    availability = Availability.query.filter_by(id=data['availabilityId']).first()
    if availability:
        availability.is_available = False

    db.session.commit()

    return jsonify({'message': 'Appointment created and availability updated'}), 201

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
        availability = Availability.query.get(appointment.availabilityId)
        if availability:
            availability.is_available = True

        db.session.delete(appointment) 
        db.session.commit()
        return jsonify({'message': 'Appointment deleted'}), 200

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
