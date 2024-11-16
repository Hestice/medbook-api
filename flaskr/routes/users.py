from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flaskr.models import db, User

bp = Blueprint('users', __name__, url_prefix='/api/users')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "User already exists"}), 400

    user = User(name=name, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 400

    login_user(user)
    return jsonify({"message": "Login successful"}), 200

@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

@bp.route('/current_user', methods=['GET'])
def get_current_user():
    if current_user.is_authenticated:
        return jsonify({
            "uuid": current_user.uuid,
            "name": current_user.name,
            "email": current_user.email,
            "role": current_user.role
        })
    else:
        return jsonify({"error": "No user is currently logged in"}), 401

@bp.route('/exists', methods=['POST'])
def user_exists():
    data = request.get_json()
    email = data.get('email')

    user = User.query.filter_by(email=email).first()
    if user is not None:
        return jsonify({"exists": True}), 200
    else:
        return jsonify({"exists": False}), 200

@bp.route('/reset_password_request', methods=['POST'])
def reset_password_request():
    data = request.get_json()
    email = data.get('email')

    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"error": "User not found"}), 400

    token = user.generate_reset_token()
    return jsonify({"token": token}), 200

@bp.route('/reset_password/<token>', methods=['POST'])
def reset_password(token):
    user = User.verify_reset_token(token)
    if not user:
        return jsonify({"error": "Invalid or expired token"}), 400

    data = request.get_json()
    password = data.get('password')
    user.set_password(password)
    db.session.commit()

    return jsonify({"message": "Password reset successful"}), 200
