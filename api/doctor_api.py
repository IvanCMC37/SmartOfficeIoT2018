from flask import Blueprint, request, jsonify
import schema
import doctor_calendar

d_mod = Blueprint("doctor_api",  __name__)


##
# GET ALL DOCTORS TEST EXAMPLE
##
@d_mod.route("/doctor", methods=["GET"])
def get_doctors():
    all_doctors = schema.Doctor.query.all()
    result = schema.doctors_schema.dump(all_doctors)
    return jsonify(result.data)

def get_docs():
    all_doctors = schema.Doctor.query.all()
    result = schema.doctors_schema.dump(all_doctors)
    return result

def select_doctor_by_id(id):
    doc = schema.Doctor.query.get(id)
    return doc

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