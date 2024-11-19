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

    if not appointment:
        return jsonify({'message': 'Appointment not found'}), 404

    new_appointment_from = datetime.strptime(data['time_start'], '%Y-%m-%d %H:%M:%S')
    new_appointment_to = datetime.strptime(data['time_end'], '%Y-%m-%d %H:%M:%S')

    if 'availabilityId' in data and data['availabilityId'] != appointment.availabilityId:
        new_availability = Availability.query.filter_by(id=data['availabilityId'], is_available=True).first()
        if not new_availability:
            return jsonify({'message': 'New availability slot not found or not available'}), 400

        if new_appointment_from < new_availability.availableFrom or new_appointment_to > new_availability.availableTo:
            return jsonify({'message': 'New appointment time falls outside of the new availability slot'}), 400

        old_availability = Availability.query.filter_by(id=appointment.availabilityId).first()
        if old_availability:
            old_availability.is_available = True

        appointment.availabilityId = new_availability.id
        new_availability.is_available = False
    else:
        current_availability = Availability.query.filter_by(id=appointment.availabilityId).first()
        if not current_availability:
            return jsonify({'message': 'Current availability slot not found'}), 400

        if new_appointment_from < current_availability.availableFrom or new_appointment_to > current_availability.availableTo:
            return jsonify({'message': 'New appointment time falls outside of the current availability slot'}), 400

    appointment.appointment_from = new_appointment_from
    appointment.appointment_to = new_appointment_to

    db.session.commit()
    return jsonify({'message': 'Appointment updated'}), 200

@bp.route('/<id>', methods=['DELETE'])
def delete_appointment(id):
    user = get_current_user_from_session()
    if not user:
        return unauthorized_message()

    appointment = Appointment.query.get(id)
    if appointment:
        availability = Availability.query.filter_by(id=appointment.availabilityId).first()
        if availability:
            availability.is_available = True
            db.session.commit()
    
        db.session.delete(appointment)
        db.session.commit()
        return jsonify({'message': 'Appointment deleted and availability restored'}), 204
    return jsonify({'message': 'Appointment not found'}), 404

@bp.route('/', methods=['GET'])
def list_appointments():
    user = get_current_user_from_session()
    if not user:
        return unauthorized_message()

    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            appointments = Appointment.query.filter(
                Appointment.appointment_from >= start_date,
                Appointment.appointment_from <= end_date
            ).all()
        except ValueError:
            return jsonify({'message': 'Invalid date format, use YYYY-MM-DD'}), 400
    else:
        appointments = Appointment.query.all()

    return jsonify([appointment.serialize() for appointment in appointments]), 200