from __future__ import print_function
from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
# import credentials

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'

# Add more token files for different doctors
# store = file.Storage('credentials/doctor_token_1.json')
# creds = store.get()
# if not creds or creds.invalid:
#     flow = client.flow_from_clientsecrets('credentials/doctor_credentials_1.json', SCOPES)
#     creds = tools.run_flow(flow, store)
# service = build('calendar', 'v3', http=creds.authorize(Http()))

# Test format
input_date=[]
input_date.append(["2018-09-30T09:00:00","2018-09-30T17:00:00"])
input_date.append(["2018-10-1T09:00:00","2018-10-1T17:00:00"])
input_date.append(["2018-10-2T09:00:00","2018-10-2T17:00:00"])
input_date.append(["2018-10-3T09:00:00","2018-10-3T17:00:00"])
input_date.append(["2018-10-4T09:00:00","2018-10-4T17:00:00"])

def token_decider(doctor_num):
    store = file.Storage('credentials/doctor_token_{}.json'.format(doctor_num))
    creds = store.get()
    if not creds or creds.invalid:
        print("Cant find")
        flow = client.flow_from_clientsecrets('credentials/doctor_credentials_{}.json'.format(doctor_num), SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    return service
    # calendar_checker(service)

def main():
    # for input_list in input_date:
    #     print(input_list[0])
    #     print(input_list[1])
    insertEvent(input_date, 1)
    # token_decider(2)

def calendar_checker(service):
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            if(calendar_list_entry['summary']=="Work Day"):
                print("Calendar already existed")
                print(calendar_list_entry['id'])
                return calendar_list_entry['id']

        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    print("New calendar needed")
    return None
        
def insertEvent(inputDate, doctor_num):
    # store = file.Storage('credentials/doctor_token_1.json')
    # creds = store.get()
    # if not creds or creds.invalid:
    #     flow = client.flow_from_clientsecrets('credentials/doctor_credentials_1.json', SCOPES)
    #     creds = tools.run_flow(flow, store)
    # service = build('calendar', 'v3', http=creds.authorize(Http()))
    service = token_decider(doctor_num)

    checker_output = calendar_checker(service)
    if(checker_output==None):
        secondaryCalendar = {
            'summary': "Work Day",
            'timeZone': 'Australia/Melbourne'
        }

        created_calendar = service.calendars().insert(body=secondaryCalendar).execute()

        print(created_calendar['id'])
        id = created_calendar['id']
    else:
        id = checker_output

    for inputDate_list in inputDate:
        time_start = inputDate_list['start_time']
        time_end = inputDate_list['end_time']
        event = {
            'summary': 'Available time for patient',
            'start': {
                'dateTime': time_start,
                'timeZone': 'Australia/Melbourne',
            },
            'end': {
                'dateTime': time_end,
                'timeZone': 'Australia/Melbourne',
            },
            'transparency': 'transparent'
        }

        event = service.events().insert(calendarId=id, body=event).execute()
        print('Event created: {}'.format(event.get('htmlLink')))

    event_checker(id,service)

def event_checker(id,service):
    # Call the Calendar API
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId=id, timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

# if __name__ == '__main__':
#     main()
