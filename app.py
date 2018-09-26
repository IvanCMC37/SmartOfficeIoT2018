#!/usr/bin/env python3
"""Main module to load the application"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from forms import AppointmentForm, PatientSearchForm
import os, schema, json, config

APP = Flask(__name__)

from api import mod
import api

bootstrap = Bootstrap(APP)
# Load from config.py
APP.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(config.username, config.password, config.ip, config.database)
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(APP)
ma = Marshmallow(APP)

APP.register_blueprint(mod, url_prefix="/api")


@APP.route("/")
def homepage():
    return render_template('home.html', title='Home')


@APP.route("/doctor", methods=['GET', 'POST'])
def index():
    search = PatientSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
 
    return render_template('doctor_index.html', form=search)

@APP.route('/results')
def search_results(search):
    results = []
    qry = None
    search_string = search.data['patient_number']
    print(search_string)
    if len(search_string)>0:
        qry = schema.User.query.get(search_string)
        print(qry)
        results =  schema.user_schema.jsonify(qry)
        # return redirect('/doctor')
    if qry==None:
        flash('No record on this patient number!')
        return redirect('/doctor')
    else:
        
        # display results
        return render_template('doctor_result.html', results=qry)


##
# PATIENT
##
@APP.route("/patient", methods=["GET", "POST"])
def patient_appointments():
    """Displays all the active appointments and allows new appointments to be made"""
    form = AppointmentForm()

    if request.method == 'POST':
        start_datetime = form.start_datetime.data
        end_datetime = form.end_datetime.data
        title = form.title.data
        api.add_patient_appointment(start_datetime, end_datetime, title)

        # need to refresh page to update appointments
        return redirect(url_for('patient_appointments'))

    # Show all appointments for current patient
    all_appointments = schema.Appointment.query.filter_by(patient_id = 1)
    result = schema.appointments_schema.dump(all_appointments)

    return render_template('patient.html', form=form, all_appointments=result.data)


## CANT FIGURE OTU DELETE
# @APP.route("/patient", methods=["POST"])
# def delete_patient_appointment():
#     """Deletes the appointment by id"""  
#     print("test??") 
#     del_id = request.form['delete_id']
#     appointment = schema.Appointment.query.get(del_id)
#     schema.db.session.delete(appointment)
#     schema.db.session.commit()
#     print("delete success!")
#     return redirect(url_for('delete_patient_appointment'))

##
# CLERK
##

@APP.route("/clerk", methods=["GET", "POST"])
def clerks_page():
    """Displays all the active appointments and allows new appointments to be made"""
    form = AppointmentForm()

    if request.method == 'POST':
        start_datetime = form.start_datetime.data
        end_datetime = form.end_datetime.data

        patient = schema.Patient.query.get(1)
        new_appointment = schema.Appointment(start_datetime, end_datetime, title, patient_id = patient.id)
        schema.db.session.add(new_appointment)
        schema.db.session.commit()

        # need to refresh page to update appointments
        return redirect(url_for('clerks_page'))

    all_appointments = schema.Appointment.query.all()
    result = schema.appointments_schema.dump(all_appointments)
    print(result)

    return render_template('clerk.html', form=form, all_appointments=result.data)


# Launch Application
if __name__ == "__main__":
    """Take only the IPv4 address for connecting"""
    ips = os.popen('hostname -I').read()
    host = ips.split(' ')
    APP.run(host=host[0], port=5000, debug=True)
    