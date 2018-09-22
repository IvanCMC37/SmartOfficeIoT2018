from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, SelectField, DateField
from flask_wtf import FlaskForm

# first is the value submitted, second value is the text shown on the UI
FAKEDATA = [("2","2:00"), ("3", "3:00"), ("4", "4:00")]


class AppointmentForm(FlaskForm):
  title = TextField('Title:', validators=[validators.required()])
  start_datetime = DateField('Date:', format ='%d/%m/%Y' , validators=[validators.required()])
  end_datetime = DateField('Time:', format ='%d/%m/%Y', validators=[validators.required()])