#!/usr/bin/env python3
"""Main module to load the application"""
from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from forms import AppointmentForm
import os, schema


APP = Flask(__name__)

bootstrap = Bootstrap(APP)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:raspberry@35.201.28.228/smartoffice'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(APP)
ma = Marshmallow(APP)
db.init_app(APP)


@APP.route("/")
def homepage():
    return render_template('home.html', title='Home')


@APP.route("/doctor")
def doctors_page():
    return render_template('doctors.html')


@APP.route("/patient", methods=["GET", "POST"])
def appointments():

    form = AppointmentForm()

    first_name = form.first_name.data
    last_name = form.last_name.data
    email = form.email.data
    specialization = form.specialization.data
    user_type = form.appointment_type.data

    new_user = schema.User(first_name, last_name, email, specialization, user_type)
    schema.db.session.add(new_user)
    schema.db.session.commit()

    all_users = schema.User.query.all()

    return render_template('patient.html', form=form, all_users=all_users)

# endpoint to get user detail by id
@APP.route("/patient/<id>", methods=["GET"])
def user_detail(id):
    user = schema.User.query.get(id)
    return schema.user_schema.jsonify(user)


@APP.route("/clerk")
def clerks_page():
    return render_template('clerks.html')


if __name__ == "__main__":
    """Take only the IPv4 address for connecting"""
    ips = os.popen('hostname -I').read()
    host = ips.split(' ')
    APP.run(host=host[0], port=5000, debug=True)

