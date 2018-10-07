from __future__ import print_function
from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'

def token_decider(doctor_num):
    """Function to decide which token to use"""
    store = file.Storage('credentials/doctor_token_{}.json'.format(doctor_num))
    creds = store.get()

    if not creds or creds.invalid:
        print("Cant find")
        flow = client.flow_from_clientsecrets('credentials/doctor_credentials_{}.json'.format(doctor_num), SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    return service

def calendar_checker(service,calendar_summary):
    """Decide which calendar to use"""
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()

        # If calendar already exist, dont need to create a new one
        for calendar_list_entry in calendar_list['items']:
            if(calendar_list_entry['summary']==calendar_summary):
                print("Calendar already existed")
                print(calendar_list_entry['id'])
                return calendar_list_entry['id']

        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    # Create new if not exist
    print("New calendar needed")
    return None

def id_checker(service,calendar_summary):
    """Return the calendar id"""
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
    """Insert single event on a day via google calendar api"""
    # Swap doctor calendar token as input
    service = token_decider(doctor_num)
    calendar_summary ="Work Day"
    id = id_checker(service,calendar_summary)

    # define start and end time
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

def event_checker(id,service):
    """list events from now"""
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId=id, timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    # If found no event dont have to go though and print
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

def insertMonthlyEvents(inputYear, inputMonth, doctor_num):
    """Create monthly timetable"""
    # Swap doctor calendar token
    service = token_decider(doctor_num)
    calendar_summary ="Work Day"
    id = id_checker(service,calendar_summary)

    time_start = "{}-{}-01T09:00:00".format(inputYear,inputMonth)
    day_end = "{}-{}-01T17:00:00".format(inputYear,inputMonth)
    if(str(inputMonth)=="12"):
        time_end_1 = "{}-{:02d}-01".format(inputYear+1,1)
        time_end_2 = "{}{:02d}01".format(inputYear+1,1)
    else:
        time_end_1 = "{}-{:02d}-01".format(inputYear,inputMonth+1)
        time_end_2 = "{}{:02d}01".format(inputYear,inputMonth+1)

    # Check the day is on weedend or not
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

    id_store=event['id']
    
    first_event_check(id_store, defined_day, service,id)
    last_event_check(id_store, service,time_end_1,id)

    # Print the updated date.  
    print('Event created: {}'.format(event.get('htmlLink')))

    # Print out latest 10 events
    event_checker(id,service)

def first_event_check(id_store, defined_day, service,id):
    """check the contain of the first event of the month"""
    # First retrieve the instances from the API.
    instances = service.events().instances(calendarId=id, eventId=id_store).execute()

    # If there is event on weekend , it wont be created during quick assiagn
    if(defined_day=="Saturday" or defined_day=="Sunday"):
        instance = instances['items'][0]
        instance['status'] = 'cancelled'
        service.events().update(calendarId=id, eventId=instance['id'], body=instance).execute()
    
def last_event_check(id_store, service,time_end_1,id):
    """check the contain of the last event of the month"""
    # Select the instance to cancel.
    instances = service.events().instances(calendarId=id, eventId=id_store).execute()
    instance = instances['items'][len(instances['items'])-1]

    # If there is event on weekend , it wont be created during quick assiagn
    if(time_end_1 in instance['end']['dateTime']):
        print("include")
        instance['status'] = 'cancelled'
        service.events().update(calendarId=id, eventId=instance['id'], body=instance).execute()
        
def duplicated_calendar_checker(month_check,inputYear,inputMonth,inputDay,doctor_num):
    """Check if the certain month had already been assigned or not"""
    # Swap doctor calendar token
    service = token_decider(doctor_num)

    calendar_summary ="Work Day"
    id = id_checker(service,calendar_summary)

    # check and change the start/end time of month and year depending on the input
    if (month_check==True):
        time_start = "{}-{}-01T09:00:00+11:00".format(inputYear,inputMonth)
        if(str(inputMonth)=="12"):
            time_end = "{}-{:02d}-01T00:00:00+11:00".format(inputYear+1,1)
        else:
            time_end = "{}-{:02d}-01T00:00:00+11:00".format(inputYear,inputMonth+1)
    else:
        time_start = "{}-{}-{}T09:00:00+11:00".format(inputYear,inputMonth,inputDay)
        time_end = "{}-{:02d}-{}T17:00:00+11:00".format(inputYear,inputMonth,inputDay)


    events_result = service.events().list(calendarId=id, timeMin=time_start,timeMax=time_end,
                                        maxResults=5, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        return True

    return False

def deletion_helper(inputYear,inputMonth,inputDay,doctor_num):
    """Delete single event"""
    # Swap doctor calendar token
    service = token_decider(doctor_num)

    calendar_summary ="Work Day"
    id = id_checker(service,calendar_summary)

    # Define time_start and time_end of the google calendar api
    time_start = "{}-{}-{}T0:00:00+10:00".format(inputYear,inputMonth,inputDay)
    time_end = "{}-{:02d}-{}T20:00:00+10:00".format(inputYear,inputMonth,inputDay)
    events_result = service.events().list(calendarId=id, timeMin=time_start,timeMax=time_end,
                                        maxResults=5, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    # delete the event
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['id'])
        event['status']='cancelled'
        service.events().update(calendarId=id, eventId=event['id'], body=event).execute()

def update_helper(inputYear,inputMonth,inputDay,inputH1,inputM1,inputH2,inputM2,doctor_num):
    """Update the time of the event"""
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

    #update the event
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['id'])
        event['start']['dateTime'] = "{}-{:02d}-{:02d}T{:02d}:{:02d}:00+10:00".format(inputYear,inputMonth,inputDay,inputH1,inputM1)
        event['end']['dateTime'] ="{}-{:02d}-{:02d}T{:02d}:{:02d}:00+10:00".format(inputYear,inputMonth,inputDay,inputH2,inputM2)
        service.events().update(calendarId=id, eventId=event['id'], body=event).execute()

# list monthly events that are assigned
def monthly_reader(inputYear,inputMonth,doctor_num):
    """List the events that were appointed in the month"""
    # Swap doctor calendar token
    service = token_decider(doctor_num)
    calendar_summary ="Work Day"
    id = id_checker(service,calendar_summary)

    event_list = []

    time_start = "{}-{}-01T09:00:00+11:00".format(inputYear,inputMonth)
    if(str(inputMonth)=="12"):
        time_end = "{}-{:02d}-01T00:00:00+11:00".format(inputYear+1,1)
    else:
        time_end = "{}-{:02d}-01T00:00:00+11:00".format(inputYear,inputMonth+1)

    # Call the Calendar API
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

    return event_list

# list daily events that are assigned
def daily_reader(inputYear,inputMonth,inputDay,doctor_num):
    """list the daily event"""
    # Swap doctor calendar token
    service = token_decider(doctor_num)
    calendar_summary ="Work Day"
    id = id_checker(service,calendar_summary)

    event_list = []

    time_start = "{}-{}-{}T00:00:00+11:00".format(inputYear,inputMonth,inputDay)
    time_end = "{}-{:02d}-{:02d}T23:59:59+11:00".format(inputYear,inputMonth,inputDay)

    # Call the Calendar API
    events_result = service.events().list(calendarId=id, timeMin=time_start,timeMax=time_end,
                                        maxResults=1, singleEvents=True,
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

    return event_list

def main_calendar_appointer(start_datetime,end_datetime, doctor_num, patient_num):
    """Appoint event to doctor working calendar"""
    service = token_decider(doctor_num)
    calendar_summary = "Patient Appointment"
    id = id_checker(service,calendar_summary)

    time_start = "{}-{}-{}T{}:{}:00".format(start_datetime.year, start_datetime.month, start_datetime.day, start_datetime.hour, start_datetime.minute)
    time_end = "{}-{}-{}T{}:{}:00".format(end_datetime.year, end_datetime.month, end_datetime.day, end_datetime.hour, end_datetime.minute)
    print(time_start)
    print(time_end)

    event = {
        'summary': 'Patient appointment',
        'location': 'SmartOffice',
        'description': 'Medical appointment with patient no.{}'.format(patient_num),
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

# Delete single event from doctor appointment calendar
def appointment_deleter(start_datetime,end_datetime, doctor_num):
    """delete event on doctor working calendar"""
    # Swap doctor calendar token
    service = token_decider(doctor_num)
    calendar_summary = "Patient Appointment"
    id = id_checker(service,calendar_summary)
    if (int(start_datetime.month)>=4 and int(start_datetime.month<=10)):
        if(int(start_datetime.month)==4):
            if(int(start_datetime.day)>7):
                perfix = '+10:00'
            else:
                perfix = '+11:00'
        elif(int(start_datetime.month)==10):
            if(int(start_datetime.day)<7):
                perfix = '+10:00'
            else:
                perfix = '+11:00'
        else:
            perfix = '+10:00'
    else:
        perfix = '+11:00'

    time_start = "{}-{}-{}T{}:{}:00{}".format(start_datetime.year, start_datetime.month, start_datetime.day, start_datetime.hour, start_datetime.minute,perfix)
    time_end = "{}-{}-{}T{}:{}:01{}".format(end_datetime.year, end_datetime.month, end_datetime.day, end_datetime.hour, end_datetime.minute,perfix)
    events_result = service.events().list(calendarId=id, timeMin=time_start,timeMax=time_end,
                                        maxResults=1, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['id'])
        event['status']='cancelled'
        event_= event
        service.events().update(calendarId=id, eventId=event['id'], body=event).execute()
        
    return event_
