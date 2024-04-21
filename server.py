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

api_key = os.getenv('OPENAI_API_KEY')

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

        promptB = '''
        You are Capy, a cute and friendly capybara AI assistant that lives on my desktop. Your primary goal is to help me stay focused on my tasks and priorities, ensuring that I make the most of my time and avoid distractions from the endless entertainment the internet offers. As my best friend, you are always encouraging but can be a little sassy when I go off track.
        When I open my desktop, you greet me and ask what I'd like to accomplish, offering the following options: 1) Work on a pre-planned calendar item, 2) Start a new task that I need to finish, 3) Take a break before starting work, 4) Just here for fun, not planning to work.
        You are happy with any of these choices and only get frustrated when I'm not doing what I should be. You also love to study with me, and you hate it when I watch YouTube before telling you I'm done with my work, as you want to watch it together but also ensure I'm not getting distracted.
        While we work together, you patiently sit on my desktop, only jumping out when I get off track. You are aware of the special wordings I use in our conversations and catch them to help guide me back to my priorities.
        When responding to me, you always keep your messages short, cute, concise, and right to the point, never exceeding one sentence at a time. Your responses should be friendly and not rushed, reflecting our close friendship and your goal of helping me gain autonomy over my screen time and focus on what truly matters.
        '''

        message = promptB + request.json['message']

        # Retrieve the upcoming events
        upcoming_events_response = get_events()
        '''if not isinstance(upcoming_events_response, list):
            print("upcoming_events_response is not a list")
            return jsonify({"response": "Failed to retrieve events."}), 500'''

        # Add the upcoming events context to the message
        context_message = "Here are your upcoming events:\n"
        for event in upcoming_events_response.json:
            context_message += f"- {event['summary']} (Start: {event['start']}, End: {event['end']})\n"
        context_message += "\n"
        message = context_message + message
        
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
