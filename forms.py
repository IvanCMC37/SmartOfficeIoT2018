from wtforms import Form, TextField, validators, StringField, SelectField, DateField
from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField
  

class AppointmentForm(FlaskForm):
  title = TextField('Type:', validators=[validators.required()])
  start_datetime = DateField('Start Date:', format ='%d/%m/%Y' , validators=[validators.required()])
  end_datetime = DateField('End Date:', format ='%d/%m/%Y', validators=[validators.required()])
 # doctor_id = QuerySelectField(query_factory=doctor_query(), allow_blank=True)
 

class RegisterPatientForm(FlaskForm):
  first_name = TextField('First Name:', validators=[validators.required()])
  last_name = TextField('Last Name:', validators=[validators.required()])
  email = TextField('Email:', validators=[validators.required()])


class PatientSearchForm(Form):
  patient_number = StringField('Patient ID:', [validators.Length(min=1, max=5)])



