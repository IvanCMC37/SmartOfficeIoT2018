from __future__ import print_function
from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('credentials/token_patient.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials/patient_credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

def main():
    insertCalendar()

def insertCalendar():
    calendar=input("Enter a Calendar Name\n")

    secondaryCalendar = {
        'summary': calendar,
        'timeZone': 'Australia/Melbourne'
    }

    created_calendar = service.calendars().insert(body=secondaryCalendar).execute()

    print(created_calendar['id'])
    insertEvent(created_calendar['id'])

def insertEvent(calendarId):
    inputDate=input("Enter a Date\n")
    time_start = "{}T09:00:00+10:00".format(inputDate)
    time_end   = "{}T17:00:00+10:00".format(inputDate)
    event = {
        'summary': 'Working',
        'start': {
            'dateTime': time_start,
            'timeZone': 'Australia/Perth',
        },
        'end': {
            'dateTime': time_end,
            'timeZone': 'Australia/Melbourne',
        },
        'transparency': 'transparent'
    }

    event = service.events().insert(calendarId=calendarId, body=event).execute()
    print('Event created: {}'.format(event.get('htmlLink')))

    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    # Call the Calendar API
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId=calendarId, timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == '__main__':
    main()
