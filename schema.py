from flask import Flask
from app import db, ma
import os

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), unique=False, nullable=False)
    last_name = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    specialization = db.Column(db.String(50), unique=False)
    user_type = db.Column(db.String(20), unique=False, nullable=False, default='patient')

    def __init__(self, first_name, last_name, email, specialization, user_type):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.specialization = specialization
        self.user_type = user_type

    # relationships reference the class. allows for additional queries to be run
    appointments = db.relationship('Appointment', backref = db.backref('user',lazy=True))
    patient_history = db.relationship('PatientHistory', backref=db.backref('user', lazy=True))

    def __repr__(self):
        return 'User(%s, %s, %s, %s, %s)' % (self.first_name, self.last_name, self.email, self.specialization, self.user_type)


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_date = db.Column(db.Date, unique = False, nullable=False)
    appointment_time = db.Column(db.Time, unique = False, nullable=False)

    # references the table name user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __init__(self, appointment_date, appointment_time, user_id):
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.user_id = user_id

    def __repr__(self):
        return 'Appointment(%s, %s, %s)' % (self.appointment_date, self.appointment_time, self.user_id)


class PatientHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String(100), unique=False, nullable=False)
    diagnoses = db.Column(db.String(50), unique=False, nullable=False)

    def __init__(self, notes, diagnoses):
        self.notes = notes
        self.diagnoses = diagnoses

    appointment_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return 'PatientHistory(%s, %s)' % (self.notes, self.diagnoses)


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('first_name', 'last_name', 'email', 'specialization', 'user_type')


class AppointmentSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('appointment_date', 'appointment_time', 'user_id')


class PatientHistorySchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('notes', 'diagnoses')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)

patient_history_schema = PatientHistorySchema()
patient_histories_schema = PatientHistorySchema(many=True)
