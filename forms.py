from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, SelectField, DateField
from flask_wtf import FlaskForm

# first is the value submitted, second value is the text shown on the UI
FAKEDATA = [("2","2:00"), ("3", "3:00"), ("4", "4:00")]

class AppointmentForm(FlaskForm):
  appointment_date = DateField('Date:', validators=[validators.required()])
  appointment_time = SelectField('Time:', choices=FAKEDATA, validators=[validators.required()])