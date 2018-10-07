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

@p_mod.route("/patientAppmts/<id>", methods=["GET"])
def get_patient_appointments(id):
    print("id---"+str(id))
    """Return appointments for patient as JSON"""
    #if id:
    all_appmts = schema.db.session.query(schema.Appointment).filter_by(patient_id=id).join(schema.Doctor).join(schema.Patient).all()
    print('all_appmts---'+str(all_appmts))
    #all_appmts = schema.Appointment.query.filter(schema.Appointment.patient_id ==id)
        
    #return schema.appointments_with_doctor_schema.jsonify(all_appmts)
    return jsonify(schema.appointments_with_doctor_schema.dump(all_appmts).data)

@p_mod.route("/doctorAppmts/<id>", methods=["GET"])
def get_doctor_appointments(id):
    print("id---"+str(id))
    """Return appointments for patient as JSON"""
    #if id:
    all_appmts = schema.db.session.query(schema.Appointment).filter_by(doctor_id=id).all()
    print('all_appmts---'+str(all_appmts))
    #all_appmts = schema.Appointment.query.filter(schema.Appointment.patient_id ==id)
        
    #return schema.appointments_with_doctor_schema.jsonify(all_appmts)
    return jsonify(schema.appointments_with_doctor_schema.dump(all_appmts).data)


def get_patient_by_object(pat):
    """Return patients by object"""
    patient = schema.Patient.query.get(pat)
    return patient


def delete_patient_appointment(del_id):
    """Deletes appointment by patient"""
    print('del_id---'+del_id)
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
    """Gets all registered patients"""
    reg_patients = schema.Patient.query.all()
    result = schema.patients_schema.dump(reg_patients)
    return result

##
# APPOINTMENTS
##
@p_mod.route("/appointment", methods=["GET"])
def all_appointments():
    """Gets all appointments"""
    all_appointments = schema.Appointment.query.all() 
    result = schema.appointments_schema.dump(all_appointments)
    return jsonify(result.data)

def add_patient_appointment(start, end, title, p_id, d_id):
    """Add patient's appointment"""
    appmt = schema.Appointment(start, end, title, patient_id = p_id, doctor_id = d_id)
    schema.db.session.add(appmt)
    schema.db.session.commit()
    result = schema.appointment_schema.dump(appmt)
    return jsonify(result.data)

##
# Patient history
##
# get patient history
@p_mod.route("/history/<id>", methods=["GET"])
def patient_detail(id):
    patient_history = schema.PatientHistory.query.get(id)
    print(patient_history)
    return schema.patient_history_schema.jsonify(patient_history)

# Edit patient history
@p_mod.route("/history/<id>", methods=["POST"])
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




