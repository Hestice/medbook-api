from dotenv import load_dotenv
from flask import Flask, logging, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    CORS(app, supports_credentials=True, origins=[os.getenv('FRONTEND_URL')])

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    session_dir = os.path.join(app.instance_path, 'sessions')
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = session_dir
    app.config['SESSION_COOKIE_NAME'] = 'session'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True

    Session(app)

    db.init_app(app)
    migrate.init_app(app, db)

    from flaskr.models import User, Availability, Appointment, Comment

    from .routes import users, availabilities, appointments, comments
    app.register_blueprint(users.bp)
    app.register_blueprint(availabilities.bp)
    app.register_blueprint(appointments.bp)
    app.register_blueprint(comments.bp)

    @app.before_request
    def log_session_data():
        app.logger.debug(f'Session: {session.items()}')

    app.logger.setLevel(logging.DEBUG)
    
    return app
