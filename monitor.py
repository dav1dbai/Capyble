import os
import pyautogui
import pathlib
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime
import textwrap
from dotenv import load_dotenv
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
import PIL.Image
#way apr 20
#sorry this get exposed since i am not sure vishnu's secure thing works
GOOGLE_API_KEY= 'AIzaSyAVQANU6aIGDc2ifwG5ZFils-hNrREoZ00'
genai.configure(api_key=GOOGLE_API_KEY)
'''
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)
'''
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))



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

def main():
    # Setup Google Calendar API
    creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/calendar.readonly'])
    service = build('calendar', 'v3', credentials=creds)

    # Take a screenshot
    screenshot_path = take_screenshot_and_save()
    print(screenshot_path)

    # Get current event description
    event_description = get_current_event_description(service)
    prompt = f"Does this screenshot match the event description: '{event_description}'?"

    img = PIL.Image.open('image.jpg')
    img

    # Initialize the Gemini API model
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content("What is the meaning of life?")
    response = model.generate_content(img)
    to_markdown(response.text)
    #https://ai.google.dev/gemini-api/docs/get-started/python 
    #the syntax is porbably a bit off, as ouputing text to text have no porblem


if __name__ == '__main__':
    main()
