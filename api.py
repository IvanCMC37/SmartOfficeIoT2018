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