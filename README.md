# Appointment Booking System
This is an appointment booking system for patients and doctors built using Flask and PostgreSQL. The system allows doctors to set their availability, and patients can book appointments based on the available time slots. The backend uses Flask for routing and PostgreSQL (hosted on Supabase) for data storage.

## Getting Started
Follow these steps to run the application locally.

1. Set up a Virtual Environment
Create a virtual environment and activate it:

Windows:
```
python -m venv venv
source venv/scripts/activate
```

Mac:
```
python3 -m venv venv
source venv/bin/activate
```

2. Install Dependencies
Install the required dependencies with:
```
pip install -r requirements.txt
```

3. Run the Flask Application
Start the Flask server with:
```
python server.py
```

4. Running Database Migrations
To run the database migrations, first export the Flask app:
```
export FLASK_APP=server.py
```

Then you can run the migration commands:
```
flask db upgrade
flask db migrate
```

## Backend Overview
The backend is built with Flask and uses PostgreSQL as the database. Authentication is handled via Flask sessions, and the app is structured with the following core models:

## Models Rundown
### User Model
Stores user details (name, email, role) and authentication data (hashed password).
Supports password reset functionality with tokens.
### Appointment Model
Represents a scheduled appointment between a patient and a doctor.
Stores the patient and doctor information, appointment time, and any comments related to the appointment.
### Availability Model
Represents a doctor's available time slots.
Stores the start and end time for each availability and whether the doctor is available.
### Comment Model
Allows users (patients or doctors) to leave comments on appointments.
Each comment is tied to a specific appointment and user.

## Database Setup
The app uses PostgreSQL hosted on Supabase (pre-deployed on Render.com), but for development, it is recommended to run the database locally.

## Running PostgreSQL Locally
If you want to run the PostgreSQL database locally:

> Install and configure PostgreSQL on your machine.
> Update your .env file with the appropriate database credentials.
> Run the Flask application as instructed above.


## Authentication
Authentication is handled through Flask sessions. The app uses cookies in the browser for session management. There is no separate authentication service; authentication is done directly through the database with hashed passwords.

## Notes
Make sure the .env file contains the appropriate keys for secret management and database connection.
I used postman to test my endpoints locally.