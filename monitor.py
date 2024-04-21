import os
import pyautogui
import pathlib
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timezone
import textwrap
from dotenv import load_dotenv
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
import PIL.Image
import time
import pytz

#need to first run quickstart and then monitor would work. check why this happens.
#need to do with the frontend

#way apr 21
#now it can takes screenshoot, and 
load_dotenv()
GOOGLE_API_KEY= os.getenv('GEMINI_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
'''
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
'''

def take_screenshot_and_save():
    screenshot = pyautogui.screenshot()
    screenshot_path = 'current_screen.png'
    screenshot.save(screenshot_path)
    return screenshot_path

def get_current_event_description(service):
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=1, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        return "No event description available."
    return events[0].get('summary', 'description' )

def is_event_happening_now(service):
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    # Getting the current UTC time
    utc_now = datetime.utcnow()

    # Converting UTC time to local time, for example
    local_timezone = pytz.timezone('America/Los_Angeles')
    local_now = utc_now.replace(tzinfo=pytz.utc).astimezone(local_timezone)

    print(local_now)
    # Get the current and next events
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=1, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    if (events):
        event_start_str = events[0].get('start').get('dateTime')
        print("Event start time:", event_start_str)
        # Parse the event start time string into a datetime object
        event_start_time = datetime.strptime(event_start_str, "%Y-%m-%dT%H:%M:%S%z")

        # Compare the parsed event start time with the local time
        if event_start_time < local_now:
            return True   
    return False  # No event is happening now or comparison fails
  
def contains_no(phrase):
    # \b around 'no' defines a word boundary, ensuring 'no' is a complete word
    return bool(re.search(r'\bno\b', phrase, re.IGNORECASE))

def check(service):
    # Take a screenshot
    screenshot_path = take_screenshot_and_save()

    # Get current event description
    event_description = get_current_event_description(service)
    prompt = f"Does this screenshot match the event description: '{event_description}'? Give Yes or No"
    img = PIL.Image.open(screenshot_path)
    
    # ask gemini if this is the same event
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([prompt,img])
    return (contains_no(phrase))
    #https://ai.google.dev/gemini-api/docs/get-started/python 


def main():
    # Setup Google Calendar API
    creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/calendar.readonly'])
    service = build('calendar', 'v3', credentials=creds)


    #about to write some logics in checking servise 
    #1 when there is an event going on, during the strat and the end time, check every 5 minutes
    while True:
      if (is_event_happening_now(service)):
          time.sleep(300)
          #print(is_event_happening_now(service))
          if (not check(service)):
            #post a thing to change the frontend
            #TO DO
            else:
              #happy Cappy
          time.sleep(300) #check every 5 minuts



    '''
    #testing gemini-pro(text only)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("What is the meaning of life?")
    print(response.text)
    '''

   
    

if __name__ == '__main__':
    main()
