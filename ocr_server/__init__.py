from  __future__  import print_function
import os
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import datetime
import pickle

#imports for Flask_SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# imports for the google calendar API
import googleapiclient.discovery
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# import our OCR function
from ocr_core import ocr_core

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():

    # define a folder to store and later serve the images
    UPLOAD_FOLDER = 'static/uploads/'

    # allow files of a specific type
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

    app = Flask(__name__)

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SECRET_KEY'] = 'secret-key-goes-here' #Login Key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # function to check the file extension
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    db.init_app(app)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
