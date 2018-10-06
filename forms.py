from wtforms import Form, TextField, validators, StringField, SelectField, DateField
from flask_wtf import FlaskForm


class AppointmentForm(FlaskForm):
  year = SelectField('year', choices=[('2018','2018'),('2019','2019')])
  month = SelectField('month', choices=[("","--None--"),("1","January"),("2","February"),("3","March"),("4","April"),("5","May"),("6","June"),("7","July"),("8","August"),("9","September"),("10","October"),("11","Novemeber"),("12","December")], validators=[validators.required()])
  day = SelectField('day', choices= [], validators=[validators.required()])
  slot = SelectField('slot',choices= [("","--None--")], validators=[validators.required()])
  patient= SelectField('patient', validators=[validators.required()])
  doctor = SelectField('doctor', validators=[validators.required()])
  #title = TextField('Type:', validators=[validators.required()])
  start_datetime = DateField('Start Date:', format ='%d/%m/%Y' , validators=[validators.required()])
  end_datetime = DateField('End Date:', format ='%d/%m/%Y', validators=[validators.required()])
 

class RegisterPatientForm(FlaskForm):
  """Define Register form"""
  first_name = TextField('First Name:', validators=[validators.required()])
  last_name = TextField('Last Name:', validators=[validators.required()])
  email = TextField('Email:', validators=[validators.required()])


class PatientSearchForm(Form):
  """Define Patient search form"""
  patient_number = StringField('Patient ID:', [validators.Length(min=1, max=5)])