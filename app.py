#!/usr/bin/env python3
"""Main module to load the application"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
from forms import AppointmentForm, PatientSearchForm, RegisterPatientForm, CalendarForm, CalendarForm_2
import os, schema, json, config
from schema import db, ma
from datetime import timedelta, datetime
import requests

APP = Flask(__name__)
import datetime
from api.patient_api import p_mod
from api.doctor_api import d_mod
from api.clerk_api import c_mod
from api import patient_api, doctor_api, clerk_api

# Load from config.py
APP.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(config.username, config.password, config.ip, config.database)
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['SECRET_KEY'] = 'secret'

doctor_choices=None

# Register api blueprints
APP.register_blueprint(p_mod, url_prefix="/api")
APP.register_blueprint(d_mod, url_prefix="/api")
APP.register_blueprint(c_mod, url_prefix="/api")
doc_list=[]
api_url= ""
server_url=""

db.init_app(APP)
ma.init_app(APP)

@APP.route("/")
def homepage():
    return render_template('home.html', title='Home')


@APP.route("/about")
def aboutpage():
    return render_template('about.html', title='About')


@APP.route("/doctor", methods=['GET', 'POST'])
def index():
    year_list = [2018,2019]
    month_list = [1,2,3,4,5,6,7,8,9,10,11,12]
    date_list = []
    date_list.extend(range(1, 32))
    doctor_id = 0
    form = CalendarForm()
    form_2 = CalendarForm_2()
    form.day.choices = [(str(x),str(x)) for x in date_list]
    form_2.day_f2.choices = [(str(x),str(x)) for x in date_list]

    doctor_infos = requests.get('{}{}'.format(api_url,"doctor")).json()
    if request.method == 'POST' and len(request.form)==1:
        print("Chose a doctor calendar")
        print(request.form['doctor_id'])
        doctor_id=int(request.form['doctor_id'])
    elif request.method == 'POST' and len(request.form)==3:
        
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


@APP.route('/doctor/appointment', methods=['GET', 'POST'])
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

        if(patient_id==None or doctor_id==None):
            print("wrong use")
        else:
            logic = True
            print(patient_id)
            print(doctor_id)

            # doctor_info not needed
            doctor_infos = requests.get('{}{}'.format(api_url,"doctor")).json()
            patient_infos = requests.get('{}{}/{}'.format(api_url,"patient",patient_id)).json()
            patient_histories = requests.get('{}{}/{}'.format(api_url,"history",patient_id)).json()
            print(patient_histories)

    return render_template('doctor_result.html',patient_histories=patient_histories,server_url=server_url,logic=logic,patient_id=patient_id,patient_infos=patient_infos,doctor_id=doctor_id, doctor_infos= doctor_infos )


##
# PATIENT
##
@APP.route("/patient", methods=["GET", "POST"])
def patient_appointments():
    print('patient GET OR POST')
    """Displays all the active appointments and allows new appointments to be made and deleted"""
    form = AppointmentForm()
    # Get all patients and generate combo box values
    patients = patient_api.get_reg_patients()
    #patient_choices=[['','--None--']]
    patient_choices=[]
    for patient in patients.data:
        patient_choices.append([patient['id'], patient['first_name'] + ' ' + patient['last_name']])
    form.patient.choices=patient_choices
    # Get all doctors and generate combo box values
    #doctors = doctor_api.get_doctors()
    doctors = requests.get('{}{}'.format(api_url,"doctor")).json()
    print("doctors---"+str(doctors))
    doctor_choices=[]
    for doctor in doctors:
        doctor_choices.append([doctor['id'], doctor['first_name'] + ' ' + doctor['last_name']])
    form.doctor.choices=doctor_choices
    # Generate Days
    date_list = [("","--None--")]
    form.day.choices = date_list
    # date_list.extend(range(1, 32))
    # form.day.choices = [(str(x),str(x)) for x in date_list]
    reg_form = RegisterPatientForm()
    

    # Set default patient to 1
    pat = patient_api.get_patient_by_object(1)
    
    if request.method == 'POST' and "delete_appmt" in request.form:
        # Deletes the appointment by id  
        del_id = request.form['delete_appmt']
        patient_api.delete_patient_appointment(del_id)
        
        return redirect(url_for('patient_appointments'))

    elif request.method == 'POST' and "book_appmt" in request.form:
        print('patient POST book_appmt')
        # Submit form of appointment booking
        #start_datetime = form.start_datetime.data
        #end_datetime = form.end_datetime.data
        doctor_id=request.form['doctor']
        
        if request.form['pat_id']:
            pat_id = request.form['pat_id']
        else:
            pat_id = 1
        print(pat_id)

        start_datetime = request.form['slot']
        print(start_datetime)
        print(type(start_datetime))
        #Thu Oct 04 2018 14:30:00 GMT+1000
        start_datetime=start_datetime.replace(' (Australian Eastern Standard Time)','')
        start_datetime= datetime.datetime.strptime(start_datetime, '%a %b %d %Y %H:%M:%S %Z%z')
        print(start_datetime)
        print(type(start_datetime))
        title = 'Patient Appointment'
        # for appmt in avail_appmts['days'] :
        #     print('appmt---'+str(appmt))
        #     start_datetime = appmt['start_time']
        #     end_datetime = appmt['end_time']
        patient_api.add_patient_appointment(start_datetime, start_datetime+timedelta(minutes=30), title, pat_id, doctor_id)
        pat = patient_api.get_patient_by_object(pat_id)
        result = patient_api.get_patient_appointments(pat_id)
        print(result)
        return render_template('patient.html', form=form, reg_form=reg_form, all_appointments=result, patients=patients.data,pat_id=pat_id)

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
        result = patient_api.get_patient_appointments(pat_id)
        pat = patient_api.get_patient_by_object(pat_id)
        return render_template('patient.html', form=form, reg_form=reg_form, all_appointments=result, patients=patients.data, pat_id=pat_id)
    
    #result = patient_api.get_patient_appointments()

    #return render_template('patient.html', form=form, reg_form=reg_form, all_appointments=result, patients=patients.data, doctors = doctors.data, pat=pat)
    return render_template('patient.html', form=form, reg_form=reg_form, patients=patients.data)


##
# CLERK
##
# @APP.route("/clerk", methods=["GET", "POST"])
# def clerks_page():
#     """Displays all the active appointments and allows new appointments to be made"""
#     form = AppointmentForm()

#     if request.method == 'POST':
#         start_datetime = form.start_datetime.data
#         end_datetime = form.end_datetime.data

#         patient = schema.Patient.query.get(1)
#         new_appointment = schema.Appointment(start_datetime, end_datetime, title, patient_id = patient.id)
#         schema.db.session.add(new_appointment)
#         schema.db.session.commit()

#         # need to refresh page to update appointments
#         return redirect(url_for('clerks_page'))

#     all_appointments = schema.Appointment.query.all()
#     result = schema.appointments_schema.dump(all_appointments)
#     print(result)

#     return render_template('clerk.html', form=form, all_appointments=result.data)



# Launch Application
if __name__ == "__main__":
    """Take only the IPv4 address for connecting"""
    ips = os.popen('hostname -I').read()
    host = ips.split(' ')
    api_url = "http://{}:{}/api/".format(host[0],5000)
    server_url = "http://{}:{}/".format(host[0],5000)
    APP.run(host=host[0], port=5000, debug=True)

