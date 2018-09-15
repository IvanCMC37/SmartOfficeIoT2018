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

    def __init__(self, first_name, last_name, email, specialization, user_type):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.specialization = specialization
        self.user_type = user_type


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_date = db.Column(db.Date, unique = False)
    appointment_time = db.Column(db.Time, unique = False)

    def __init__(self, appointment_date, appointment_time):
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    user = db.relationship('User', backref = db.backref('users',lazy=True))


class AppointmentHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String(100), unique=False)
    diagnoses = db.Column(db.String(50), unique=False)

    def __init__(self, notes, diagnoses):
        self.notes = notes
        self.diagnoses = diagnoses

    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    appointment = db.relationship('Appointment', backref = db.backref('appointments', lazy=True))


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('first_name', 'last_name', 'email', 'specialization', 'user_type')

class AppointmentSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('appointment_date', 'appointment_time')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)
