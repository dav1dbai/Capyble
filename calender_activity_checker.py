import os
import io
import requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from PIL import Image
import pytesseract

# Set up Google Calendar API credentials from Way
creds = Credentials.from_authorized_user_file('path/to/credentials.json', ['https://www.googleapis.com/auth/calendar.readonly']) # HAVE TO REPLACE THESE 2 VALUES

# Initialize the Calendar API service
service = build('calendar', 'v3', credentials=creds)

def get_current_event():
    # Get the current time
    now = datetime.utcnow().isoformat() + 'Z'

    # Fetch events from the user's primary calendar
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=1, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        return None
    return events[0]

def read_screenshot():
    # Take a screenshot using a screenshot library (e.g., PyAutoGUI)
    # Replace this with the actual code to take a screenshot
    screenshot = Image.open('current_screen.png') # HAVE TO CHANGE THIS

    # Extract text from the screenshot using OCR (e.g., pytesseract)
    text = pytesseract.image_to_string(screenshot)

    return text

def fetch_gemini_data(symbol):
    """
    Fetch trading data for a given symbol from the Gemini API.
    """
    url = f'https://api.gemini.com/v1/pubticker/{symbol.lower()}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for {symbol}. Status code: {response.status_code}")
        return None

def compare_event_and_screenshot(event_summary, screenshot_text):
    """
    Check if the event summary is related to the data extracted from the screenshot.
    This function needs to be customized based on how you define 'resemblance' between
    the event summary and the screenshot data.
    """
    # Example: Check if the event summary is mentioned in the screenshot text
    return event_summary.lower() in screenshot_text.lower()


def main():
    event = get_current_event()
    if event:
        screenshot_text = read_screenshot()
        # Assuming the event summary contains the symbol for which we want to fetch data
        symbol = event['summary'].split()[-2]  # Adjust this as needed
        gemini_data = fetch_gemini_data(symbol)
        if gemini_data and compare_event_and_screenshot(event['summary'], screenshot_text):
            print("Good job")
        else:
            print("The screenshot does not match the calendar event or failed to fetch Gemini data.")
    else:
        print("No upcoming events found.")
if __name__ == '__main__':
    main()