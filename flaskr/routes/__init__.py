from flask import Blueprint

bp = Blueprint('main', __name__)

# Import models to register them with SQLAlchemy
from flaskr.models import Patient, Doctor, Appointment