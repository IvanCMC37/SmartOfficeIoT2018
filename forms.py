from wtforms import Form, TextField, validators, StringField, SelectField
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
  

class AppointmentForm(FlaskForm):
  title = TextField('Type:', validators=[validators.required()])
  start_datetime = DateField('Start Date:', format ='%d/%m/%Y' , validators=[validators.required()])
  end_datetime = DateField('End Date:', format ='%d/%m/%Y', validators=[validators.required()])
 

class RegisterPatientForm(FlaskForm):
  first_name = TextField('First Name:', validators=[validators.required()])
  last_name = TextField('Last Name:', validators=[validators.required()])
  email = TextField('Email:', validators=[validators.required()])


class PatientSearchForm(Form):
  patient_number = StringField('Patient ID:', [validators.Length(min=1, max=5)])