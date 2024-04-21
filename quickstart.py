import datetime
import os.path

#file written by way, arp 20 2024
#deplaying the next 10 items, add and delete eventsn (noticing its deleted by ID at this moment and may need to figure out some logics in futrue)
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Global variable declaration for the service
global service

def create_event(summary, location, description, start_time, end_time):
    """Create a new event on the user's primary calendar."""
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/Los_Angeles',  # Adjust the timezone as necessary
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/Los_Angeles',  # Adjust the timezone as necessary
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    try:
        created_event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (created_event.get('htmlLink')))
    except HttpError as error:
        print(f"An error occurred: {error}")
    
def delete_event(event_id):
    """Delete an event from the user's primary calendar."""
    try:
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        print("Event deleted successfully.")
    except HttpError as error:
        print(f"An error occurred: {error}")
        if error.resp.status == 404:
            print("The event was not found.")


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
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

    try:
        # Call the Calendar API
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
        else:
            # Prints the start, end, and name of the next 10 events
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                end = event['end'].get('dateTime', event['end'].get('date'))
                id = event['id']
                print(start, end, id, event["summary"])

    except HttpError as error:
        print(f"An error occurred: {error}")

    # Example usage: Create a new event
    create_event(
        'Team Meeting',
        'Office',
        'Discuss project updates',
        '2024-04-21T09:00:00-07:00',
        '2024-04-21T10:00:00-07:00'
    )
    delete_event('1jjk52l04qku1j1gaqstmpkuhm')

if __name__ == "__main__":
    main()
