from dotenv import load_dotenv
from flask import Flask
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
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    db.init_app(app)
    migrate.init_app(app, db)

    from flaskr.models import User, Availability, Appointment, Comment

    from .routes import users, availabilities, appointments, comments
    app.register_blueprint(users.bp)
    app.register_blueprint(availabilities.bp)
    app.register_blueprint(appointments.bp)
    app.register_blueprint(comments.bp)

    return app