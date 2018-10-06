from wtforms import Form, TextField, validators, StringField, SelectField, DateField
from flask_wtf import FlaskForm


class AppointmentForm(FlaskForm):
  year = SelectField('year', choices=[('2018','2018'),('2019','2019')])
  month = SelectField('month', choices=[("1","1"),("2","2"),("3","3"),("4","4"),("5","5"),("6","6"),("7","7"),("8","8"),("9","9"),("10","10"),("11","11"),("12","12")])
  day = SelectField('day',choices= [])
  #slot = SelectField('slot', validators=[validators.required()])
  patient= SelectField('patient', validators=[validators.required()])
  doctor = SelectField('doctor', validators=[validators.required()])
  #title = TextField('Type:', validators=[validators.required()])
  start_datetime = DateField('Start Date:', format ='%d/%m/%Y' , validators=[validators.required()])
  end_datetime = DateField('End Date:', format ='%d/%m/%Y', validators=[validators.required()])
 

class RegisterPatientForm(FlaskForm):
  first_name = TextField('First Name:', validators=[validators.required()])
  last_name = TextField('Last Name:', validators=[validators.required()])
  email = TextField('Email:', validators=[validators.required()])


class PatientSearchForm(Form):
  patient_number = StringField('Patient ID:', [validators.Length(min=1, max=5)])