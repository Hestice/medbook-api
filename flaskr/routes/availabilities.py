from flask import Blueprint, request, jsonify
from datetime import datetime, time
from flaskr.models import User, db, Availability
from .utils import get_current_user_from_session, paginate, unauthorized_message

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

@bp.route('/', methods=['GET'])
def list_availabilities():
    user = get_current_user_from_session()
    if not user or user.role != 'doctor':
        return unauthorized_message()

    availabilities = Availability.query.filter_by(doctorId=user.uuid).all()
    return jsonify([availability.serialize() for availability in availabilities]), 200

@bp.route('/patient', methods=['GET'])
def list_patient_availabilities():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    availabilities_query = Availability.query.filter_by(is_available=True)
    paginated_data = paginate(availabilities_query, page, per_page)

    return jsonify({
        'total': paginated_data['total'],
        'page': paginated_data['page'],
        'per_page': paginated_data['per_page'],
        'availabilities': [availability.serialize() for availability in paginated_data['items']]
    }), 200

@bp.route('/doctor/<uuid>', methods=['GET'])
def get_doctor(uuid):
    user = get_current_user_from_session()
    if not user:
        return unauthorized_message()

    doctor = User.query.filter_by(uuid=uuid).first()
    if not doctor:
        return jsonify({'message': 'Doctor not found'}), 404

    return jsonify({
        'uuid': doctor.uuid,
        'name': doctor.name
    }), 200