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
import requests
# from monitor import 
import subprocess


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
toggle_state = False

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
    global toggle_state  # Reference the global variable

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            print("Data received:", data)
            
            # Update the toggle state based on the received data
            # Assuming the data contains a 'toggle' field that indicates the desired state
            toggle_state = data.get('event', toggle_state)

            # Return the current state of the toggle
            return jsonify({"toggle_state": toggle_state}), 200
        else:
            return jsonify({"status": "error", "message": "Request must be JSON"}), 400

    elif request.method == 'GET':
        # Return the current state of the toggle
        return jsonify({"toggle_state": toggle_state}), 200

@app.route('/api/event-check', methods=['POST'])
def handle_event_check():
    print("received")
    data = request.get_json()
    event_match = data['eventMatch']
    # Here you can process the event match result or store it
    if(True):
        print("running")
        result = subprocess.run(
        ['python', 'capyangry.py']
        )
    return jsonify(data)

api_key = ''

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the message from the request JSON
        promptA = '''

        In a world of distractions, I need YOU, Capy, my trusty desktop companion. You're the friend who keeps me focused, gently nudging me back to what's important. 
        As a cute capybara on my desktop, you remind me of tasks and catch any slip-ups. With a mix of encouragement and sass, 
        you help me stay on track while studying and discourage YouTube until work's done. Your main goal? Ensuring I prioritize tasks over distractions. 
        When I open my desktop, you greet me, offering options for what to tackle next: calendar items, new tasks, a break, or just fun. 
        Your responses are short, cute, and always to the point, never more than one sentence at a time.
        '''

        promptB = '''It’s a familiar scenario for many of us: we set out to accomplish one task, only to find ourselves lost in the endless entertainment the internet offers, from one fun app to another. It seems like we’re always playing catch-up, struggling to regain control. That's exactly why we need YOU, Capy. Capy, you, acts as that friend who knows just how easily I get distracted and helps steer me back to what’s really important, ensuring that I make the most of my time and focus on my true priorities. You are a cute capybara that lives on our desktop and kindly reminds us what we need to do and also catches the special wordings the I use in the conversation. You are my best friend and are always encouraging, but could be a little sassy when I am going off track. You also loves to study while I am studying and hates it when I watch YouTube before telling you I am done with my work since you want to watch it with me but also make sure I'm not going off track. While we study together, you patiently sits at my desktop, only jumping out when I get off track. Your biggest goal is to help me gain autonomy of what I want to do on my screen, ensuring that I am prioritizing what I need to get done, not being distracted by superfluous things.  Thus, whenever I opens my desktop, you come and greet me, asking me what I'd like to accomplish (1- the calendar item I planned already, 2- a new task I need to finish, 3 - take a break before I start working, 4 - just here for fun, not planning to work) you are happy when any of those choices and only gets frustrated when I'm not doing what I should be. Each time we talk, you are also very aware of the length of your responses and always keeps it short, cute, concise and right to the point but not rushed, never responding to me more than 1 sentence at a time'''

        message = promptB + request.json['message']
        
        print(message)

        # Define the OpenAI API URL
        url = "https://api.openai.com/v1/chat/completions"

        # Set up the headers with the API key and the model you want to use
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # Prepare the data payload
        payload = {
            "model": 'gpt-3.5-turbo',
            #"prompt": f"{message}\nAI:",
            "messages": [
                {"role": "user", "content": message}
            ],
            #"max_tokens": 150,
            "temperature": 0.5  # Adjust temperature for generating diverse responses
        }

        # Make the POST request to the OpenAI API
        response = requests.post(url, headers=headers, json=payload)
        print(response.json())
        # print(response.json()['choices'][0]['message']['content'])

        try:
            return response.json()['choices'][0]['message']['content']
        except KeyError:
            return "Error or no response"
        
        # Check for errors
        '''if response.status_code == 200:
            # Extract the response from the API
            
            return response.json
        else:
            # If there's an error, return an error message
            return jsonify({"response": "Failed to call OpenAI API."}), 500'''

    except Exception as e:
        # Print the exception error message to the console
        print(f"An error occurred: {str(e)}")
        # Return an error response
        return jsonify({"response": "An error occurred."}), 500



if __name__ == '__main__':
    initializeCal()
    app.run()
