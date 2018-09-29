from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, SelectField, DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf import FlaskForm
import schema


class AppointmentForm(FlaskForm):
  title = TextField('Type:', validators=[validators.required()])
  start_datetime = DateField('Start Date:', format ='%d/%m/%Y' , validators=[validators.required()])
  end_datetime = DateField('End Date:', format ='%d/%m/%Y', validators=[validators.required()])
  doctor_id = QuerySelectField('Doctors', query_factory = lambda: schema.Doctor.query.all(), allow_blank=False )
 

class RegisterPatientForm(FlaskForm):
  first_name = TextField('First Name:', validators=[validators.required()])
  last_name = TextField('Last Name:', validators=[validators.required()])
  email = TextField('Email:', validators=[validators.required()])


class PatientSearchForm(Form):
  patient_number = StringField('Patient ID:', [validators.Length(min=1, max=5)])
  