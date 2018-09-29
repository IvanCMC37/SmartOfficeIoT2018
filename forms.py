from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, SelectField, DateField
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm

# first is the value submitted, second value is the text shown on the UI
FAKEDATA = [("2","2:00"), ("3", "3:00"), ("4", "4:00")]


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
  