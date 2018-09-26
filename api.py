from flask import Blueprint, request, jsonify
import schema

mod = Blueprint("api",  __name__)


##
# PATIENT
##
@mod.route("/patient", methods=["GET"])
def patient_appointments():
    all_patients = schema.Patient.query.all() 
    result = schema.patients_schema.dump(all_patients)
    return jsonify(result.data)

# endpoint to get patient detail by id
@mod.route("/patient/<id>", methods=["GET"])
def appointment_detail(id):
    patient = schema.Patient.query.get(id)
    return schema.patient_schema.jsonify(patient)


##
# APPOINTMENTS
##
@mod.route("/appointments", methods=["GET"])
def all_appointments():
    all_appointments = schema.Appointment.query.all() 
    result = schema.appointments_schema.dump(all_appointments)
    return jsonify(result.data)

def add_patient_appointment(start, end, title):
    patient = schema.Patient.query.get(1)
    doctor = schema.Doctor.query.get(1)
    appmt = schema.Appointment(start, end, title, patient_id = patient.id, doctor_id = doctor.id )
    schema.db.session.add(appmt)
    schema.db.session.commit()
    result = schema.appointment_schema.dump(appmt)
    return jsonify(result.data)

##
# Patient history
##
# get patient history
@mod.route("/history/<id>", methods=["GET"])
def patient_detail(id):
    patient_history = schema.PatientHistory.query.get(id)
    print(patient_history)
    return schema.patient_history_schema.jsonify(patient_history)

# Edit patient history
@mod.route("/history/<id>", methods=["POST"])
def patient_history_update(id):
    user = schema.PatientHistory.query.get(id)
    diagnoses = request.json['diagnoses']
    notes = request.json['notes']
    date =request.json['date']

    user.diagnoses = diagnoses
    user.notes = notes
    user.date = date

    schema.db.session.commit()
    return schema.patient_history_schema.jsonify(user)
# doctor calander event api 



# ##
# # CLERK
# ##
# @mod.route("/clerk", methods=["GET"])
# def clerk_appointments(appmt):
#     patient()



# ##
# # DOCTOR
# ##



##
# GET ALL DOCTORS TEST EXAMPLE
##
@mod.route("/doctor", methods=["GET"])
def get_doctors():
    all_doctors = schema.Doctor.query.all()
    result = schema.doctors_schema.dump(all_doctors)
    return jsonify(result.data)