from flask import Flask
from flask_sqlalchemy import SQLAlchemy


#needs to be same instance of flask app
API = Flask(__name__)
API.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:raspberry@35.201.28.228/smartoffice-216206:australia-southeast1:smartoffice-db'
API.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(API)

