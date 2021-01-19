# general imports
from  __future__  import print_function
import os
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import datetime
import pickle
from flask import Blueprint

#imports for Flask_SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# imports for the google calendar API
import googleapiclient.discovery
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# import our OCR function
from ocr_core import ocr_core


#main = Blueprint('main', __name__)


# define a folder to store and later serve the images
UPLOAD_FOLDER = 'static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


app = Flask(__name__)

# Setting the configurations for the flask app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# route and function to handle the home page
@app.route('/')
def home_page():
    return render_template('index.html')

# route and function to handle the upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):
            filenameSecure = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filenameSecure))

            # call the OCR function on it
            extracted_text = ocr_core(file)

            print(filenameSecure)

            # extract the text and display it
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=extracted_text,
                                   img_src=app.config['UPLOAD_FOLDER'] + filenameSecure)
    elif request.method == 'GET':
        return render_template('upload.html')

@app.route('/calendar')
def calendar_page():
    creds =  None
    SCOPES  = ['https://www.googleapis.com/auth/calendar.readonly']
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with  open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            # with open('token.pickle', 'wb') as token: # can't write files in Google App Engine so comment out or delete
            # pickle.dump(creds, token)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

    service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() +  'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        print('No upcoming events found.')
    # for event in events:
    # start = event['start'].get('dateTime', event['start'].get('date'))
    # print(start, event['summary'])
    event_list = [event["summary"] for event in events]

    return  render_template("calendar.html", events=event_list)

@app.route('/user')
def user_page():
    a_clients = [["Client: John", "Passport: Y", "College: N"],["Client: Harry", "Passport: N", "College: N"],["Client: Tania", "Passport: Y", "College: Y"]]
    return render_template("user.html", a_clients = a_clients)

@app.route('/profile')
def profile():
    return 'Profile'


if __name__ == '__main__':
    app.run()
    #app.create_app()
