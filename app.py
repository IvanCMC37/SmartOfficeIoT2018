#!/usr/bin/env python3
"""Main module to load the application"""
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import os

APP = Flask(__name__)
bootstrap = Bootstrap(APP)


@APP.route("/")
def homepage():
    return render_template('home.html', title='Home')


@APP.route("/doctor")
def doctors_page():
    return render_template('doctors.html')


@APP.route("/patient")
def get_appointments():
    return render_template('patient.html')

@APP.route("/patient", methods=["POST"])
def add_appointment():
    return render_template('patient.html')


@APP.route("/clerk")
def clerks_page():
    return render_template('clerks.html')


if __name__ == "__main__":
    """Take only the IPv4 address for connecting"""
    ips = os.popen('hostname -I').read()
    host = ips.split(' ')
    APP.run(host=host[0], port=5000, debug=True)

