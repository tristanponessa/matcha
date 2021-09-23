import sys
sys.path.append('/home/user/Documents/coding/matcha')
sys.path.append('/home/user/Documents/coding/matcha/matcha_app')
sys.path.append('/home/user/Documents/coding/matcha/matcha_app/test')

import matcha_app.fields
import matcha_app.db

import os

SECRET_KEY = os.urandom(32)# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))# Enable debug mode.
DEBUG = True# Connect to the database
DB = 'sqlite'
SQLALCHEMY_DATABASE_URI = 'your psycopg2 URI connection'# Turn off the Flask-SQLAlchemy event system and warning
SQLALCHEMY_TRACK_MODIFICATIONS = False