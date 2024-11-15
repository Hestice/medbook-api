from flask import Blueprint, jsonify, request
from ..models import Patient, db

bp = Blueprint('patients', __name__, url_prefix='/patients')

@bp.route('/', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    return jsonify([{'id': patient.id, 'name': patient.name, 'contact_info': patient.contact_info} for patient in patients])

@bp.route('/', methods=['POST'])
def add_patient():
    data = request.get_json()
    new_patient = Patient(id=data['id'], name=data['name'], contact_info=data['contact_info'])
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({'message': 'Patient added'}), 201
