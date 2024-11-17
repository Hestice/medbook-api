from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import Serializer
import uuid
import os

class User(db.Model):
    __tablename__ = 'users'
    uuid = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_reset_token(self, expires_in=600):
        s = Serializer(os.getenv('SECRET_KEY'), expires_in)
        return s.dumps({'reset_password': self.uuid}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(os.getenv('SECRET_KEY'))
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['reset_password'])
    
    def get_id(self):
        return self.uuid

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.String, primary_key=True)
    patientId = db.Column(db.String, db.ForeignKey('users.uuid'), nullable=False)
    doctorId = db.Column(db.String, db.ForeignKey('users.uuid'), nullable=False)
    availabilityId = db.Column(db.String, db.ForeignKey('availabilities.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    time = db.Column(db.Time, nullable=False)
    comments = db.relationship('Comment', backref='appointment', lazy=True)


class Availability(db.Model):
    __tablename__ = 'availabilities'
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    doctorId = db.Column(db.String(50), nullable=False)
    availableFrom = db.Column(db.Time, nullable=False)
    availableTo = db.Column(db.Time, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'doctorId': self.doctorId,
            'availableFrom': self.availableFrom.strftime('%Y-%m-%d %H:%M:%S'),
            'availableTo': self.availableTo.strftime('%Y-%m-%d %H:%M:%S')  
        }

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.String, primary_key=True)
    appointmentId = db.Column(db.String, db.ForeignKey('appointments.id'), nullable=False)
    userId = db.Column(db.String, db.ForeignKey('users.uuid'), nullable=False)
    content = db.Column(db.String, nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
