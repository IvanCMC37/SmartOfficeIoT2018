from flask import Blueprint, request, jsonify
import schema

p_mod = Blueprint("patient_api",  __name__)

##
# PATIENT
##
@p_mod.route("/patient", methods=["GET"])
def get_patients():
    """Returns JSON of all patients"""
    all_patients = schema.Patient.query.all() 
    result = schema.patients_schema.dump(all_patients)
    return jsonify(result.data)

# endpoint to get patient detail by id
@p_mod.route("/patient/<id>", methods=["GET"])
def appointment_detail(id):
    """Returns JSON of a single patient"""
    patient = schema.Patient.query.get(id)
    return schema.patient_schema.jsonify(patient)

def get_patient_appointments(*id):
    """Return appointments for patient as JSON"""
    if id:
        all_appmts = schema.Appointment.query.filter_by(patient_id = id)    
    else:
        # Loads appointments for first patient by default
        all_appmts = schema.Appointment.query.filter_by(patient_id = 1)
        

    result = schema.appointments_schema.dump(all_appmts)
    return result

def delete_patient_appointment(del_id):
    appointment = schema.Appointment.query.get(del_id)
    schema.db.session.delete(appointment)
    schema.db.session.commit()

def reg_patient(first, last, email):
    """Registers a new patient"""
    patient = schema.Patient(first, last, email)
    schema.db.session.add(patient)
    schema.db.session.commit()
    result = schema.patient_schema.dump(patient)
    return jsonify(result.data)

def get_reg_patients():
    reg_patients = schema.Patient.query.all()
    result = schema.patients_schema.dump(reg_patients)
    return result

##
# APPOINTMENTS
##
@p_mod.route("/appointment", methods=["GET"])
def all_appointments():
    all_appointments = schema.Appointment.query.all() 
    result = schema.appointments_schema.dump(all_appointments)
    return jsonify(result.data)

def add_patient_appointment(start, end, title):
    ## NEED TO ADD FUNCTIONALITY TO CHOOSE DOCTOR AND CREATE APPOINTMENT BASED ON PATIENT

    appmt = schema.Appointment(start, end, title, patient_id = 1, doctor_id = 1 )
    schema.db.session.add(appmt)
    schema.db.session.commit()
    result = schema.appointment_schema.dump(appmt)
    return jsonify(result.data)
