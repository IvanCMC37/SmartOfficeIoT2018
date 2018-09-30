from flask import Blueprint, request, jsonify
import schema

d_mod = Blueprint("doctor_api",  __name__)

import doctor_calendar
##
# GET ALL DOCTORS TEST EXAMPLE
##
@d_mod.route("/doctor", methods=["GET"])
def get_doctors():
    all_doctors = schema.Doctor.query.all()
    result = schema.doctors_schema.dump(all_doctors)
    return jsonify(result.data)

##
# Patient history
##
# get specific patient history(s)
@d_mod.route("/history/<id>", methods=["GET"])
def patient_detail(id):
    patient_history = schema.PatientHistory.query.filter(schema.PatientHistory.patient_id ==id)
    return schema.patient_histories_schema.jsonify(patient_history)

# Get all history 
@d_mod.route("/history", methods=["GET"])
def all_history():
    patient_histories = schema.PatientHistory.query.all()
    return schema.patient_histories_schema.jsonify(patient_histories)

# Add new patient history
@d_mod.route("/history", methods=["POST"])
def add_patient_history():
    user = request.json['id']
    diagnoses = request.json['diagnoses']
    notes = request.json['notes']
    date =request.json['date']

    new_history = schema.PatientHistory(notes = notes,diagnoses = diagnoses,date =date, patient_id =user)

    schema.db.session.add(new_history)
    schema.db.session.commit()
    return schema.patient_history_schema.jsonify(new_history)

# doctor calander event api 
@d_mod.route("/assign", methods=["POST"])
def add_availabiliy():
    input_json = request.json
    year = input_json['year']
    month = input_json['month']
    day = input_json['day']
    hour_1 = input_json['hour_1']
    hour_2 = input_json['hour_2']
    minute_1 = input_json['minute_1']
    minute_2 = input_json['minute_2']
    doctor_id = input_json['doctor_id']

    # print("Total {} event(s) will be added.".format(len(input_date['Allocated_dates'])))

    doctor_calendar.insertEvent(input_json,int(doctor_id))

    return jsonify(input_json)

@d_mod.route("/quick_assign", methods=["POST"])
def add_monthly_availability():
    input_json = request.json
    year = input_json['year']
    month = input_json['month']
    doctor_id = input_json['doctor_id']
    print("Quick assigning monthly event for Doctor No.{} on {}-{}".format(doctor_id,year,month))
    doctor_calendar.insertEvent_2(int(year),int(month),int(doctor_id))

    return jsonify(input_json)

@d_mod.route("/duplicated_check", methods=["POST"])
def duplicated_check():
    input_json = request.json
    print(len(input_json))
    if(len(input_json)==8):
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