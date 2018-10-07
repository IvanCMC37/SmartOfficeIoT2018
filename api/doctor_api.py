from flask import Blueprint, request, jsonify
import schema
from datetime import datetime,timedelta
d_mod = Blueprint("doctor_api",  __name__)

import doctor_calendar
import requests

##
# GET ALL DOCTORS TEST EXAMPLE
##
@d_mod.route("/doctor", methods=["GET"])
def get_doctors():
    all_doctors = schema.Doctor.query.all()
    result = schema.doctors_schema.dump(all_doctors)
    return jsonify(result.data)

# doctor calander event api 
@d_mod.route("/doctor/assign", methods=["POST"])
def add_availabiliy():
    input_json = request.json
    doctor_id = input_json['doctor_id']

    doctor_calendar.insertEvent(input_json,int(doctor_id))

    return jsonify(input_json)

@d_mod.route("/doctor/quick_assign", methods=["POST"])
def add_monthly_availability():
    input_json = request.json
    year = input_json['year']
    month = input_json['month']
    doctor_id = input_json['doctor_id']

    print("Quick assigning monthly event for Doctor No.{} on {}-{}".format(doctor_id,year,month))
    doctor_calendar.insertMonthlyEvents(int(year),int(month),int(doctor_id))

    return jsonify(input_json)

@d_mod.route("/doctor/duplicated_check", methods=["POST"])
def duplicated_check():
    input_json = request.json
    print(len(input_json))

    if(len(input_json)>3):
        day = input_json['day']
        month_check = False
    else:
        day= 1
        month_check = True

    year = input_json['year']
    month = input_json['month']
    doctor_id = input_json['doctor_id']

    respond=doctor_calendar.duplicated_calendar_checker(month_check,int(year),int(month),int(day),int(doctor_id))

    return jsonify(respond)

@d_mod.route("/doctor/delete_event", methods=["POST"])
def delete_action():
    input_json = request.json
    print(len(input_json))
    day = input_json['day']
    year = input_json['year']
    month = input_json['month']
    doctor_id = input_json['doctor_id']

    doctor_calendar.deletion_helper(int(year),int(month),int(day),int(doctor_id))

    return jsonify(input_json)

@d_mod.route("/doctor/update_event", methods=["POST"])
def update_action():
    input_json = request.json
    print(len(input_json))
    day = input_json['day']
    year = input_json['year']
    month = input_json['month']
    hour_1 = input_json['hour_1']
    hour_2 = input_json['hour_2']
    minute_1 = input_json['minute_1']
    minute_2 = input_json['minute_2']
    doctor_id = input_json['doctor_id']

    doctor_calendar.update_helper(int(year),int(month),int(day),int(hour_1),int(minute_1),int(hour_2),int(minute_2),int(doctor_id))

    return jsonify(input_json)

# Api to return list of event time of the month
@d_mod.route("/doctor/monthly_check", methods=["POST"])
def monthly_check():
    input_json = request.json
    print(len(input_json))
    year = input_json['year']
    month = input_json['month']
    doctor_id = input_json['doctor_id']

    respond=doctor_calendar.monthly_reader(int(year),int(month),int(doctor_id))

    return jsonify({'days': respond})

# Api to return list of event time of the day
@d_mod.route("/doctor/daily_check", methods=["POST"])
def daily_check():
    input_json = request.json
    print(len(input_json))
    year = input_json['year']
    month = input_json['month']
    day = input_json['day']
    doctor_id = input_json['doctor_id']

    respond=doctor_calendar.daily_reader(int(year),int(month),int(day),int(doctor_id))

    return jsonify({'days': respond})

@d_mod.route("/doctor/appoint_gcalendar", methods=["POST"])
def appoint_gcalendar():
    input_json = request.json
    start_datetime = input_json['start_datetime']
    
    start_datetime = start_datetime.replace("+10:00","")
    start_datetime = start_datetime.replace("+11:00","")
    
    start_datetime = datetime.strptime(start_datetime,"%Y-%m-%d %H:%M:%S")
    
    doctor_id = input_json['doctor_id']
    patient_id = input_json['patient_id']
    end_datetime = start_datetime + timedelta(minutes = 30)
    
    print(start_datetime)
    print(end_datetime)
    event=doctor_calendar.main_calendar_appointer(start_datetime,end_datetime,int(doctor_id), int(patient_id))

    return jsonify(event)

@d_mod.route("/doctor/delete_gcalendar", methods=["POST"])
def delete_gcalendar():
    input_json = request.json
    print(input_json)
    appointment_id = input_json['appointment_id']
    r = requests.get("/api/{}/{}".format("appointment", appointment_id)).json()
    start_datetime = datetime.strptime(r['start_datetime'],"%Y-%m-%d %H:%M:%S")
    doctor_id = r['doctor_id']
    end_datetime = datetime.strptime(r['end_datetime'],"%Y-%m-%d %H:%M:%S")
    print(doctor_id)
    print(start_datetime)
    print(end_datetime)
    event=doctor_calendar.appointment_deleter(start_datetime,end_datetime,int(doctor_id))

    return jsonify(event)
