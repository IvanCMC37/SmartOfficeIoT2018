"""Main module to load the application"""
from flask import Flask
APP = Flask(__name__)


@APP.route("/")
def hello():
    """Load the homepage"""
    return "<h1>Hello World</h1>"


if __name__ == "__main__":
    APP.run(debug=True, host='192.168.1.4', port=5000)

# run application using flask run --host <ip-address> OR python3 app.py and set ip address in file
# to start virtual environment. Run 'source venv/bin/activate'. To stop run 'deactivate'
