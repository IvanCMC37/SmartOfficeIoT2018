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


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('first_name', 'last_name', 'email', 'specialization', 'user_type')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
