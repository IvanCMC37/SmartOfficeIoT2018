from flask import Flask
from app import db, ma
import os

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), unique=False)
    last_name = db.Column(db.String(30), unique=False)
    email = db.Column(db.String(120), unique=True)
    specialization = db.Column(db.String(50), unique=False)
    user_type = db.Column(db.String(20), unique=False)

    appointments = db.relationship('Appointment', backref = db.backref('user',lazy=True))
    patient_history = db.relationship('PatientHistory', backref=db.backref('user', lazy=True))

    def __init__(self, first_name, last_name, email, specialization, user_type):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.specialization = specialization
        self.user_type = user_type


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_datetime = db.Column(db.DateTime, unique = False)
    end_datetime = db.Column(db.DateTime, unique = False)
    title = db.Column(db.String(255), unique = False)

    def __init__(self, start_datetime, end_datetime, user_id, title):
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.user_id = user_id
        self.title = title

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)


class PatientHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String(100), unique=False)
    diagnoses = db.Column(db.String(50), unique=False)

    def __init__(self, notes, diagnoses):
        self.notes = notes
        self.diagnoses = diagnoses

    appointment_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('first_name', 'last_name', 'email', 'specialization', 'user_type')


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

appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)

patient_history_schema = PatientHistorySchema()
patient_histories_schema = PatientHistorySchema(many=True)
