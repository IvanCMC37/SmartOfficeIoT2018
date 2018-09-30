#!/usr/bin/env python3
"""Main module to load the application"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from forms import AppointmentForm, PatientSearchForm, RegisterPatientForm
import os, schema, json, config

APP = Flask(__name__)

from api.patient_api import p_mod
from api.doctor_api import d_mod
from api.clerk_api import c_mod
from api import patient_api, doctor_api, clerk_api


bootstrap = Bootstrap(APP)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(config.username, config.password, config.ip, config.database)
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(APP)
ma = Marshmallow(APP)

APP.register_blueprint(p_mod, url_prefix="/api")
APP.register_blueprint(d_mod, url_prefix="/api")
APP.register_blueprint(c_mod, url_prefix="/api")



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
    search_string = search.data['patient_number']
    print(search_string)
    if len(search_string)>0:
        qry = schema.Patient.query.get(search_string)
        results =  schema.patient_schema.jsonify(qry)
    
    if qry==None:
        flash('No results found!')
        return redirect('/doctor')
    else:
        
        # display results
        return render_template('doctor_result.html', results=qry)


##
# PATIENT
##
@APP.route("/patient", methods=["GET", "POST"])
def patient_appointments():
    """Displays all the active appointments and allows new appointments to be made and deleted"""
    form = AppointmentForm()
    reg_form = RegisterPatientForm()
    
    if request.method == 'POST' and "delete_appmt" in request.form:
        # Deletes the appointment by id  
        del_id = request.form['delete_appmt']
        patient_api.delete_patient_appointment(del_id)
        
        return redirect(url_for('patient_appointments'))

    elif request.method == 'POST' and "book_appmt" in request.form:
        # Submit form of appointment booking
        start_datetime = form.start_datetime.data
        end_datetime = form.end_datetime.data
        title = form.title.data
        
        # p_id = request.form['select_patient']
        patient_api.add_patient_appointment(start_datetime, end_datetime, title)
        
        return redirect(url_for('patient_appointments'))   

    elif request.method == 'POST' and "reg_patient" in request.form:
        # Register a patient
        first_name = reg_form.first_name.data
        last_name = reg_form.last_name.data
        email = reg_form.email.data
        patient_api.reg_patient(first_name, last_name, email)

        return redirect(url_for('patient_appointments'))
    
    elif request.method == 'POST' and 'select_patient' in request.form:
        # Select a patient from the combo box and display appointments
        pat_id = request.form['select_patient']
        patients = patient_api.get_reg_patients()
        result = patient_api.get_patient_appointments(pat_id)
        return render_template('patient.html', form=form, reg_form=reg_form, all_appointments=result.data, patients=patients.data) 
    
    result = patient_api.get_patient_appointments()
    
    # Get all patients and generate combo box values
    patients = patient_api.get_reg_patients()

    return render_template('patient.html', form=form, reg_form=reg_form, all_appointments=result.data, patients=patients.data)




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

