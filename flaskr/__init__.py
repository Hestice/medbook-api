from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models to register them with SQLAlchemy
    from flaskr.models import Patient, Doctor, Appointment
    
    from .routes import patients, doctors, appointments
    app.register_blueprint(patients.bp)
    app.register_blueprint(doctors.bp)
    app.register_blueprint(appointments.bp)

    return app