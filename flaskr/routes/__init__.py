from flask import Blueprint

bp = Blueprint('main', __name__)

from flaskr.models import User, Appointment, Availability, Comment