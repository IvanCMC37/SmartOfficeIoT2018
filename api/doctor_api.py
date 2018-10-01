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

def get_docs():
    all_doctors = schema.Doctor.query.all()
    result = schema.doctors_schema.dump(all_doctors)
    return result

def select_doctor_by_id(id):
    doc = schema.Doctor.query.get(id)
    return doc