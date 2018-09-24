from flask import Blueprint, request, jsonify
import schema

mod = Blueprint("api",  __name__)


##
# PATIENT
##
@mod.route("/patient", methods=["GET"])
def patient_appointments():
    all_appointments = schema.Appointment.query.all()   
    result = schema.appointments_schema.dump(all_appointments)

    return jsonify(result.data)

def add_patient_appointment(appmt):
    schema.db.session.add(appmt)
    schema.db.session.commit()
    result = schema.appointment_schema.dump(appmt)
    return jsonify(result.data)

# endpoint to get user detail by id
@mod.route("/patient/<id>", methods=["GET"])
def appointment_detail(id):
    appointment = schema.Appointment.query.get(id)
    return schema.appointment_schema.jsonify(appointment)



# ##
# # CLERK
# ##
# @mod.route("/clerk", methods=["GET"])
# def clerk_appointments(appmt):
#     patient()



##
# FAKE USER
##
@mod.route("/user", methods=["GET"])
def get_users():
    all_users = schema.User.query.all()
    result = schema.users_schema.dump(all_users)
    return jsonify(result.data)

@mod.route("/user/<id>", methods=["GET"])
def user_detail(id):
    user = schema.User.query.get(id)
    return schema.user_schema.jsonify(user)

@mod.route("/user", methods=["POST"])
def add_user():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    specialization = request.json['specialization']
    user_type = request.json['user_type']

    new_user = schema.User(first_name, last_name, email, specialization, user_type)
    schema.db.session.add(new_user)
    schema.db.session.commit()
    result = schema.user_schema.dump(new_user)
    return jsonify(result)