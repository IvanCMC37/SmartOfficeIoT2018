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

def get_docs_iterable():
    all_doctors = schema.Doctor.query.all()
    return all_doctors