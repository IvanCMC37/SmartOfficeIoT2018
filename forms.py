from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, SelectField, DateTimeField

# first is the value submitted, second value is the text shown on the UI
DOCTORS = [("123","James Mcgregor"), ("1233", "John Snow"), ("1243", "Justin Bieber")]

class AppointmentForm(Form):
    first_name = TextField('First Name:', validators=[validators.required()])
    last_name = TextField('Last Name:', validators=[validators.required()])
    doctor = SelectField('Doctor:', choices=DOCTORS, validators=[validators.required()])
    date = DateTimeField('Date/Time:', validators=[validators.required()])
    appointment_type = TextField('Appointment Type:', validators=[validators.required()])
    # content = forms.CharField(max_length=256)
    # created_at = forms.DateTimeField()