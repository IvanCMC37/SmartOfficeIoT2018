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
input_date.append(["2018-10-1T09:00:00","2018-10-1T17:00:00"])


def token_decider(doctor_num):
    store = file.Storage('credentials/doctor_token_{}.json'.format(doctor_num))
    creds = store.get()
    if not creds or creds.invalid:
        print("Cant find")
        flow = client.flow_from_clientsecrets('credentials/doctor_credentials_{}.json'.format(doctor_num), SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    return service

def main():
    # monthly_reader(2018,12,1)
    main_calendar_appointer(1, 1)
#     deletion_helper(2018,10,6,1)
    # update_helper(2018,9,30,9,30,16,30,2)
#     print(duplicated_calendar_checker(2018,12,2))
    # for input_list in input_date:
    #     print(input_list[0])
    #     print(input_list[1])
    # insertEvent_2(2019,2, 1)
    # token_decider(2)

def calendar_checker(service,calendar_summary):
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            if(calendar_list_entry['summary']==calendar_summary):
                print("Calendar already existed")
                print(calendar_list_entry['id'])
                return calendar_list_entry['id']

        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    print("New calendar needed")
    return None

def id_checker(service,calendar_summary):
    # Check if secondary Calendar already existed
    checker_output = calendar_checker(service,calendar_summary)
    if(checker_output==None):
        secondaryCalendar = {
            'summary': calendar_summary,
            'timeZone': 'Australia/Melbourne'
        }

        created_calendar = service.calendars().insert(body=secondaryCalendar).execute()

        print(created_calendar['id'])
        id = created_calendar['id']
    else:
        id = checker_output
    
    return id

def insertEvent(input_json, doctor_num):
    # Swap doctor calendar token
    service = token_decider(doctor_num)
    calendar_summary ="Work Day"
    id = id_checker(service,calendar_summary)

    # for inputDate_list in inputDate:
    time_start = "{}-{}-{}T{}:{}:00".format(input_json['year'],input_json['month'],input_json['day'],input_json['hour_1'],input_json['minute_1'])
    time_end = "{}-{}-{}T{}:{}:00".format(input_json['year'],input_json['month'],input_json['day'],input_json['hour_2'],input_json['minute_2'])
    print(time_start)
    print(time_end)
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

    # Print out latest 10 events
    event_checker(id,service)

# list 10 events from now
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

# Create monthly timetable
def insertEvent_2(inputYear, inputMonth, doctor_num):
    # Swap doctor calendar token
    service = token_decider(doctor_num)
    calendar_summary ="Work Day"
    id = id_checker(service,calendar_summary)

    time_start = "{}-{}-01T09:00:00".format(inputYear,inputMonth)
    day_end = "{}-{}-01T17:00:00".format(inputYear,inputMonth)
    if(str(inputMonth)=="12"):
        # print("input is on dec")
        time_end_1 = "{}-{:02d}-01".format(inputYear+1,1)
        time_end_2 = "{}{:02d}01".format(inputYear+1,1)
    else:
        # print("normal route")
        time_end_1 = "{}-{:02d}-01".format(inputYear,inputMonth+1)
        time_end_2 = "{}{:02d}01".format(inputYear,inputMonth+1)
    # print(time_end_2)

    day = datetime.strptime(time_start+'Z', '%Y-%m-%dT%H:%M:%SZ')
    defined_day = '{0:%A}'.format(day)
    
    event = {
            'summary': 'Available time for patient',
            'start': {
                'dateTime': time_start,
                'timeZone': 'Australia/Melbourne',
            },
            'end': {
                'dateTime': day_end,
                'timeZone': 'Australia/Melbourne',
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;BYDAY=MO,TU,WE,TH,FR;UNTIL={}'.format(time_end_2)   
            ],
            'transparency': 'transparent'
    }

    event = service.events().insert(calendarId=id, body=event).execute()

    # print(event['id'])
    id_store=event['id']
    # # First retrieve the instances from the API.
    # instances = service.events().instances(calendarId=id, eventId=id_store).execute()
    # # print(instances['items'][0])
    # if(defined_day=="Saturday" or defined_day=="Sunday"):
    #     instance = instances['items'][0]
    #     instance['status'] = 'cancelled'
    #     updated_instance = service.events().update(calendarId=id, eventId=instance['id'], body=instance).execute()
    
    first_event_check(id_store, defined_day, service,id)
    last_event_check(id_store, service,time_end_1,id)
    # # Select the instance to cancel.
    # instance = instances['items'][len(instances['items'])-1]
    # if(time_end_1 in instance['end']['dateTime']):
    #     print("include")
    #     instance['status'] = 'cancelled'
    # else:
    #     print("not included")

    # updated_instance = service.events().update(calendarId=id, eventId=instance['id'], body=instance).execute()

    # Print the updated date.
    
    print('Event created: {}'.format(event.get('htmlLink')))

    # Print out latest 10 events
    event_checker(id,service)

def first_event_check(id_store, defined_day, service,id):
    # First retrieve the instances from the API.
    instances = service.events().instances(calendarId=id, eventId=id_store).execute()
    # print(instances['items'][0])
    if(defined_day=="Saturday" or defined_day=="Sunday"):
        instance = instances['items'][0]
        instance['status'] = 'cancelled'
        service.events().update(calendarId=id, eventId=instance['id'], body=instance).execute()
    
def last_event_check(id_store, service,time_end_1,id):
    # Select the instance to cancel.
    instances = service.events().instances(calendarId=id, eventId=id_store).execute()
    instance = instances['items'][len(instances['items'])-1]
    if(time_end_1 in instance['end']['dateTime']):
        print("include")
        instance['status'] = 'cancelled'
        service.events().update(calendarId=id, eventId=instance['id'], body=instance).execute()
        
def duplicated_calendar_checker(month_check,inputYear,inputMonth,inputDay,doctor_num):
    # Swap doctor calendar token
    service = token_decider(doctor_num)

    calendar_summary ="Work Day"
    id = id_checker(service,calendar_summary)

    if (month_check==True):
        # now = datetime.utcnow().isoformat() + 'Z'
        time_start = "{}-{}-01T09:00:00+11:00".format(inputYear,inputMonth)
        if(str(inputMonth)=="12"):
            # print("input is on dec")
            time_end = "{}-{:02d}-01T00:00:00+11:00".format(inputYear+1,1)
        else:
            # print("normal route")
            time_end = "{}-{:02d}-01T00:00:00+11:00".format(inputYear,inputMonth+1)
    else:
         # now = datetime.utcnow().isoformat() + 'Z'
        time_start = "{}-{}-{}T09:00:00+11:00".format(inputYear,inputMonth,inputDay)
        time_end = "{}-{:02d}-{}T17:00:00+11:00".format(inputYear,inputMonth,inputDay)
   

    # time_1 ="2018-09-01T00:00:00Z"
    # time_2 ="2018-10-01T00:00:00Z"
    print(time_end)
    events_result = service.events().list(calendarId=id, timeMin=time_start,timeMax=time_end,
                                        maxResults=5, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        return True
    return False

    # else:
    #     print("not included")

    # updated_instance = service.events().update(calendarId=id, eventId=instance['id'], body=instance).execute()

def deletion_helper(inputYear,inputMonth,inputDay,doctor_num):
    # Swap doctor calendar token
    service = token_decider(doctor_num)

    calendar_summary ="Work Day"
    id = id_checker(service,calendar_summary)

    # now = datetime.utcnow().isoformat() + 'Z'
    time_start = "{}-{}-{}T0:00:00+10:00".format(inputYear,inputMonth,inputDay)
    time_end = "{}-{:02d}-{}T20:00:00+10:00".format(inputYear,inputMonth,inputDay)
    events_result = service.events().list(calendarId=id, timeMin=time_start,timeMax=time_end,
                                        maxResults=5, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['id'])
        event['status']='cancelled'
        service.events().update(calendarId=id, eventId=event['id'], body=event).execute()

def update_helper(inputYear,inputMonth,inputDay,inputH1,inputM1,inputH2,inputM2,doctor_num):
    # Swap doctor calendar token
    service = token_decider(doctor_num)

    calendar_summary ="Work Day"
    id = id_checker(service,calendar_summary)

    time_start = "{}-{}-{}T09:00:00+10:00".format(inputYear,inputMonth,inputDay)
    time_end = "{}-{:02d}-{}T17:00:00+10:00".format(inputYear,inputMonth,inputDay)
    events_result = service.events().list(calendarId=id, timeMin=time_start,timeMax=time_end,
                                        maxResults=5, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['id'])
        # print(event['start']['dateTime'])
        event['start']['dateTime'] = "{}-{:02d}-{:02d}T{:02d}:{:02d}:00+10:00".format(inputYear,inputMonth,inputDay,inputH1,inputM1)
        event['end']['dateTime'] ="{}-{:02d}-{:02d}T{:02d}:{:02d}:00+10:00".format(inputYear,inputMonth,inputDay,inputH2,inputM2)
        service.events().update(calendarId=id, eventId=event['id'], body=event).execute()

# list monthly events that are assigned
def monthly_reader(inputYear,inputMonth,doctor_num):
    # Swap doctor calendar token
    service = token_decider(doctor_num)
    calendar_summary ="Work Day"
    id = id_checker(service,calendar_summary)

    event_list = []

    # now = datetime.utcnow().isoformat() + 'Z'
    time_start = "{}-{}-01T09:00:00+11:00".format(inputYear,inputMonth)
    if(str(inputMonth)=="12"):
        # print("input is on dec")
        time_end = "{}-{:02d}-01T00:00:00+11:00".format(inputYear+1,1)
    else:
        # print("normal route")
        time_end = "{}-{:02d}-01T00:00:00+11:00".format(inputYear,inputMonth+1)

    # Call the Calendar API
    # now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming  events')
    events_result = service.events().list(calendarId=id, timeMin=time_start,timeMax=time_end,
                                        maxResults=30, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    print('Total {} events in {}-{}'.format(len(events),inputYear,inputMonth))

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        print(start, end)
        eventObj ={}
        eventObj['start_time'] = start
        eventObj['end_time'] = end
        event_list.append(eventObj)
    # print(event_list)
    # print(len(event_list))
    return event_list

def main_calendar_appointer(input_json, doctor_num):
    service = token_decider(doctor_num)
    calendar_summary ="Patient Appointment"
    id = id_checker(service,calendar_summary)
    # for inputDate_list in inputDate:
    time_start = "{}-{}-{}T{}:{}:00".format(input_json['year'],input_json['month'],input_json['day'],input_json['hour_1'],input_json['minute_1'])
    time_end = "{}-{}-{}T{}:{}:00".format(input_json['year'],input_json['month'],input_json['day'],input_json['hour_2'],input_json['minute_2'])
    print(time_start)
    print(time_end)
    event = {
        'summary': 'Patient appointment',
        'location': 'SmartOffice',
        'description': 'Medical appointment with patient no.{}'.format(input_json['id']),
        'start': {
            'dateTime': time_start,
            'timeZone': 'Australia/Melbourne',
        },
        'end': {
            'dateTime': time_end,
            'timeZone': 'Australia/Melbourne',
        }
    }
    event_= event

    event = service.events().insert(calendarId=id, body=event).execute()
    print('Event created: {}'.format(event.get('htmlLink')))

    # Print out latest 10 events
    event_checker(id,service)
    return event_


if __name__ == '__main__':
    main()
