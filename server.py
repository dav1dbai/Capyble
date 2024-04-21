import os
from supabase import create_client, Client
from sprite_rendering import wx_sprite
import wx
import random
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import Flask,jsonify,request
from flask_cors import CORS
import json
# from monitor import 

app = Flask(__name__)
app.app_context().push()
CORS(app)

SCOPES = ["https://www.googleapis.com/auth/calendar"]
global service

url: str = "https://kjrtaohycygzmncqlffw.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtqcnRhb2h5Y3lnem1uY3FsZmZ3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTM2MDc5OTQsImV4cCI6MjAyOTE4Mzk5NH0.2lsH0yuwL6-puxJl-YULVzaaHfHtMRvD__xait4iKto"
supabase: Client = create_client(url, key)

#TODO: remove api keys

# def spriteIdle():

def initializeCal():
    global service
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)

@app.route('/events')
def get_events():
    # Call the Calendar API
    try:
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        print("Getting the upcoming 10 events")
        events_result = service.events().list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        ).execute()
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return jsonify([])
        else:
            event_json = []
            # Prints the start, end, and name of the next 10 events
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                end = event['end'].get('dateTime', event['end'].get('date'))
                id = event['id']
                print(start, end, id, event["summary"])
                event_json.append({
                    'start': start,
                    'end': end,
                    'summary': event["summary"]
                })
            return jsonify(event_json)
    except HttpError as error:
        print(f"An error occurred: {error}")
        return jsonify([])

@app.route('/sprites', methods=['POST','GET'])
def receive_data():
    if request.is_json:
        data = request.get_json()
        print("Data received:", data)
        # Assuming you want to store the data for the React component to fetch
        with open('data.json', 'w') as f:
            json.dump(data, f)
        return jsonify({"status": "success", "message": "Data received"}), 200
    else:
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400

@app.route('/api/event-check', methods=['POST'])
def handle_event_check():
    data = request.get_json()
    event_match = data['eventMatch']
    # Here you can process the event match result or store it
    return jsonify({'success': True, 'received': event_match})



if __name__ == '__main__':
    initializeCal()
    app.run()
    #sprite.jump()
