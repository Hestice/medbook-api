from flask import Blueprint, jsonify, request
from ..models import Doctor, db

bp = Blueprint('doctors', __name__, url_prefix='/doctors')

@bp.route('/', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    return jsonify([{'id': doctor.id, 'name': doctor.name, 'specialty': doctor.specialty} for doctor in doctors])

@bp.route('/', methods=['POST'])
def add_doctor():
    data = request.get_json()
    new_doctor = Doctor(id=data['id'], name=data['name'], specialty=data['specialty'])
    db.session.add(new_doctor)
    db.session.commit()
    return jsonify({'message': 'Doctor added'}), 201
