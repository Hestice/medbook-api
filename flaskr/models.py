from . import db

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    contact_info = db.Column(db.String, nullable=False)
    appointments = db.relationship('Appointment', backref='patient', lazy=True)

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    specialty = db.Column(db.String, nullable=False)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.String, primary_key=True)
    patient_id = db.Column(db.String, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.String, db.ForeignKey('doctors.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    comments = db.Column(db.String)
