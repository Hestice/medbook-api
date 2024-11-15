from flask import Blueprint, jsonify, request
from datetime import datetime
from ..models import Appointment, Patient, Doctor, db

bp = Blueprint('appointments', __name__, url_prefix='/appointments')

@bp.route('/', methods=['POST'])
def create_appointment():
    data = request.get_json()
    date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    time = datetime.strptime(data['time'], '%H:%M').time()
    patient_id = data['patient_id']
    doctor_id = data['doctor_id']
    comments = data.get('comments', '')

    # Check for overbooking
    existing_appointment = Appointment.query.filter_by(date=date, time=time, doctor_id=doctor_id).first()
    if existing_appointment:
        return jsonify({'message': 'Doctor is already booked at this time'}), 400

    new_appointment = Appointment(date=date, time=time, patient_id=patient_id, doctor_id=doctor_id, comments=comments)
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment created'}), 201

@bp.route('/<appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    data = request.get_json()
    appointment = Appointment.query.get_or_404(appointment_id)

    if 'date' in data:
        appointment.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    if 'time' in data:
        appointment.time = datetime.strptime(data['time'], '%H:%M').time()
    if 'patient_id' in data:
        appointment.patient_id = data['patient_id']
    if 'doctor_id' in data:
        appointment.doctor_id = data['doctor_id']
    if 'comments' in data:
        appointment.comments = data['comments']

    # Check for overbooking if date and time were updated
    existing_appointment = Appointment.query.filter_by(date=appointment.date, time=appointment.time, doctor_id=appointment.doctor_id).first()
    if existing_appointment and existing_appointment.id != appointment.id:
        return jsonify({'message': 'Doctor is already booked at this time'}), 400

    db.session.commit()
    return jsonify({'message': 'Appointment updated'})

@bp.route('/<appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment deleted'})

@bp.route('/', methods=['GET'])
def get_appointments():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({'message': 'Start date and end date are required'}), 400

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    appointments = Appointment.query.filter(Appointment.date.between(start_date, end_date)).all()
    return jsonify([{
        'id': appointment.id,
        'date': appointment.date.strftime('%Y-%m-%d'),
        'time': appointment.time.strftime('%H:%M'),
        'patient_id': appointment.patient_id,
        'doctor_id': appointment.doctor_id,
        'comments': appointment.comments
    } for appointment in appointments])
