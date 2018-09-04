"""Main module to load the application"""
from flask import Flask
APP = Flask(__name__)


@APP.route("/")
def homepage():
    return "<h1>Hello World</h1>"


@APP.route("/doctors")
def doctors_page():
    return "<h2>doctors page</h2>"


@APP.route("/patients")
def patients_page():
    return "<h2>patients page"


@APP.route("/clerks")
def clerks_page():
    return "<h2>clerks page"


if __name__ == "__main__":
    APP.run(debug=True, host='192.168.1.4', port=5000)

# run application using flask run --host <ip-address> OR python3 app.py and set ip address in file
# to start virtual environment. Run 'source venv/bin/activate'. To stop run 'deactivate'
