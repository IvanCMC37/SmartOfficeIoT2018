from flask import Blueprint, request, jsonify
import schema

d_mod = Blueprint("doctor_api",  __name__)

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
# @d_mod.route("/assign_work", method=["POST"])
