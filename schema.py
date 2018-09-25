from flask import Flask
from app import db, ma
import os


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), unique=False, nullable=False)
    last_name = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # specialization = db.Column(db.String(50), unique=False)
    # user_type = db.Column(db.String(20), unique=False, nullable=False, default='patient')

    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    # relationships reference the class. allows for additional queries to be run
    appointments = db.relationship('Appointment', backref = db.backref('user',lazy=True))
    patient_history = db.relationship('PatientHistory', backref=db.backref('user', lazy=True))

    def __repr__(self):
        return 'User(%s, %s, %s)' % (self.first_name, self.last_name, self.email)


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), unique=False, nullable=False)
    last_name = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    specialization = db.Column(db.String(50), unique=False)

    def __init__(self, first_name, last_name, email, specialization):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.specialization = specialization

    appointments = db.relationship('Appointment', backref = db.backref('doctor',lazy=True))

    def __repr__(self):
        return 'Doctor(%s, %s, %s, %s)' % (self.first_name, self.last_name, self.email, self.specialization)


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_datetime = db.Column(db.DateTime, unique = False)
    end_datetime = db.Column(db.DateTime, unique = False)
    title = db.Column(db.String(255), unique = False)

    def __init__(self, start_datetime, end_datetime, title, user_id, doctor_id):
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.title = title
        self.user_id = user_id
        self.doctor_id = doctor_id
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

    def __repr__(self):
        return 'Appointment(%s, %s, %s, %s, %s)' % (self.start_datetime, self.end_datetime, self.title, self.user_id, self.doctor_id)


class PatientHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String(100), unique=False, nullable=False)
    diagnoses = db.Column(db.String(50), unique=False, nullable=False)

    def __init__(self, notes, diagnoses):
        self.notes = notes
        self.diagnoses = diagnoses

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return 'PatientHistory(%s, %s)' % (self.notes, self.diagnoses)


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('first_name', 'last_name', 'email')


class DoctorSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('first_name', 'last_name', 'email', 'specialization')


class AppointmentSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('start_datetime', 'end_datetime', 'title')


class PatientHistorySchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('notes', 'diagnoses')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

doctor_schema = DoctorSchema()
doctors_schema = DoctorSchema(many=True)

appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)

patient_history_schema = PatientHistorySchema()
patient_histories_schema = PatientHistorySchema(many=True)
