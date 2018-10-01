#!/usr/bin/env python3
"""Main module to load the application"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from wtforms_sqlalchemy.fields import QuerySelectField
from forms import AppointmentForm, PatientSearchForm,CalendarForm,CalendarForm_2
import os, schema, json, config
APP = Flask(__name__)
import datetime
from api.patient_api import p_mod
from api.doctor_api import d_mod
from api.clerk_api import c_mod
from api import patient_api, doctor_api, clerk_api
import requests
bootstrap = Bootstrap(APP)
# Load from config.py
APP.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(config.username, config.password, config.ip, config.database)
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(APP)
ma = Marshmallow(APP)

APP.register_blueprint(p_mod, url_prefix="/api")
APP.register_blueprint(d_mod, url_prefix="/api")
APP.register_blueprint(c_mod, url_prefix="/api")
doc_list=[]
api_url= ""
server_url=""

@APP.route("/")
def homepage():
    return render_template('home.html', title='Home')


@APP.route("/doctor", methods=['GET', 'POST'])
def index():
    # print(api_url)
    year_list = [2018,2019]
    month_list = [1,2,3,4,5,6,7,8,9,10,11,12]
    date_list = []
    date_list.extend(range(1, 32))
    # print(date_list)
    doctor_id = 0
    form = CalendarForm()
    form_2 = CalendarForm_2()
    form.day.choices = [(str(x),str(x)) for x in date_list]
    form_2.day_f2.choices = [(str(x),str(x)) for x in date_list]

    doctor_infos = requests.get('{}{}'.format(api_url,"doctor")).json()
    # print(request.form)
    # print(len(request.form))
    if request.method == 'POST' and len(request.form)==1:
        print("Chose a doctor calendar")
        print(request.form['doctor_id'])
        doctor_id=int(request.form['doctor_id'])
    elif request.method == 'POST' and len(request.form)==3:
        # print(len(request.form))
        # print("Quick Assign Form")
        
        print(request.form)
        month = request.form['month']
        year = request.form['year']
        doctor_id = int(request.form['doctor_id'])
        print(doctor_id)
        input = {
            "month":month,
            "year":year,
            "doctor_id":doctor_id
        }
        dup_check = requests.post('{}{}'.format(api_url,"doctor/duplicated_check"),json=input).json()
        if dup_check== False:
            r = requests.post('{}{}'.format(api_url,"doctor/quick_assign"),json=input)
        else:
            flash("{}-{} already creadted, can't create again!!!".format(year,month))
    elif request.method == 'POST' and len(request.form)==8:
        print(request.form)
        month = request.form['month']
        year = request.form['year']
        day = request.form['day']
        hour_1 = request.form['hour_1']
        minute_1 = request.form['minute_1']
        hour_2 = request.form['hour_2']
        minute_2 = request.form['minute_2']
        doctor_id = int(request.form['doctor_id'])
        print(doctor_id)

        input = {
            "month":month,
            "year":year,
            "day":day,
            "hour_1":hour_1,
            "hour_2":hour_2,
            "minute_1": minute_1,
            "minute_2":minute_2,
            "doctor_id":doctor_id
        }
        dup_check = requests.post('{}{}'.format(api_url,"doctor/duplicated_check"),json=input).json()
        if dup_check== False:
            print("you can add")
            r = requests.post('{}{}'.format(api_url,"doctor/assign"),json=input)
        else:
            print("you can edit")
            r = requests.post('{}{}'.format(api_url,"doctor/update_event"),json=input)
    elif request.method == 'POST' and len(request.form)==4:
        print(request.form)
        month = request.form['month_f2']
        year = request.form['year_f2']
        day = request.form['day_f2']
        doctor_id = int(request.form['doctor_id'])
        print(doctor_id)
        input = {
            "month":month,
            "year":year,
            "day":day,
            "doctor_id":doctor_id
        }
        dup_check = requests.post('{}{}'.format(api_url,"doctor/duplicated_check"),json=input).json()
        if dup_check== False:
            flash("{}-{}-{} doesn't have any event to be deleted.".format(year,month,day))
        else:
            print("you can delete")
            r = requests.post('{}{}'.format(api_url,"doctor/delete_event"),json=input)
    else:
        print("Normal GET request")
 
    return render_template('doctor_calendar.html',form_2=form_2,form=form,doctor_id=doctor_id, doctor_infos= doctor_infos,year_list =year_list,month_list= month_list,date_list=date_list)


@APP.route('/doctor/a', methods=['GET', 'POST'])
def doctor_page_2():
    doctor_id = 0
    doctor_infos = requests.get('{}{}'.format(api_url,"doctor")).json()
    patient_infos = requests.get('{}{}'.format(api_url,"patient")).json()
    if request.method == 'POST' and len(request.form)==1:
        print("Chose a doctor calendar")
        print(request.form['doctor_id'])
        doctor_id=int(request.form['doctor_id'])
    elif request.method == 'POST' :
        doctor_id=int(request.form['doctor_id'])
        patient_id=int(request.form['patient_id'])
        print("Proceeding to patient history page...")

        return redirect(url_for('doctor_page_3',patient_id=patient_id,doctor_id=doctor_id))
        # return render_template('doctor_result.html',patient_id=patient_id,patient_infos=patient_infos,doctor_id=doctor_id, doctor_infos= doctor_infos )
    # print(request.form)
    return render_template('doctor_appointment.html',patient_infos=patient_infos,doctor_id=doctor_id, doctor_infos= doctor_infos )

@APP.route('/doctor/result', methods=['GET', 'POST'])
def doctor_page_3():
    logic = False
    doctor_infos=[]
    patient_infos=[]
    if request.method == 'POST':
        logic = True
        print(request.form)
        doctor_id = int(request.form['doctor_id'])
        patient_id = int(request.form['patient_id'])
        doctor_infos = requests.get('{}{}'.format(api_url,"doctor")).json()
        patient_infos = requests.get('{}{}/{}'.format(api_url,"patient",patient_id)).json()
        print(len(patient_infos))
        now = datetime.datetime.now()
        defined_day = now.strftime("%Y-%m-%d")
        print(defined_day)
        # print(patient_infos['first_name'])
        input ={
            "id":patient_id,
            "notes":request.form['notes'],
            "diagnoses": request.form['diagnoses'],
            "date":defined_day
        }
        r = requests.post('{}{}'.format(api_url,"history"),json=input)
        patient_histories = requests.get('{}{}/{}'.format(api_url,"history",patient_id)).json()
        print(patient_histories)
    else:
        doctor_id = request.args.get('doctor_id')
        patient_id = request.args.get('patient_id')
        
        patient_histories = []
        # print(server_url)
        if(patient_id==None or doctor_id==None):
            print("wrong use")
            # return redirect(url_for('doctor_page_2'))
        else:
            logic = True
            print(patient_id)
            print(doctor_id)
            # doctor_info not needed
            doctor_infos = requests.get('{}{}'.format(api_url,"doctor")).json()
            patient_infos = requests.get('{}{}/{}'.format(api_url,"patient",patient_id)).json()
            print(len(patient_infos))
            # print(patient_infos['first_name'])
            patient_histories = requests.get('{}{}/{}'.format(api_url,"history",patient_id)).json()
            print(patient_histories)

    return render_template('doctor_result.html',patient_histories=patient_histories,server_url=server_url,logic=logic,patient_id=patient_id,patient_infos=patient_infos,doctor_id=doctor_id, doctor_infos= doctor_infos )


##
# PATIENT
##
@APP.route("/patient", methods=["GET", "POST"])
def patient_appointments():
    """Displays all the active appointments and allows new appointments to be made and deleted"""
    form = AppointmentForm()

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
        patient_api.add_patient_appointment(start_datetime, end_datetime, title)
        
        return redirect(url_for('patient_appointments'))   

    # Gets all appoinments in list format and json format from api
    all_appointments = patient_api.get_patient_appointments()
    result = patient_api.get_patient_appointments_json()

    return render_template('patient.html', form=form, all_appointments=result.data)




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
    api_url = "http://{}:{}/api/".format(host[0],5000)
    server_url = "http://{}:{}/".format(host[0],5000)
    APP.run(host=host[0], port=5000, debug=True)
    