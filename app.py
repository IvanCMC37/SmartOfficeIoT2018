"""Main module to load the application"""
from flask import Flask, render_template

APP = Flask(__name__)
APP.config['TESTING'] = True


@APP.route("/")
def homepage():
    return render_template('home.html', title='Home')


@APP.route("/doctors")
def doctors_page():
    return render_template('doctors.html')


@APP.route("/patients")
def patients_page():
    return render_template('patients.html')


@APP.route("/clerks")
def clerks_page():
    return render_template('clerks.html')


if __name__ == "__main__":
    APP.run(debug=True, host='10.132.96.234', port=5000)

