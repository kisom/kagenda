"""cal implements an interface to the Google Calendar API."""
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from kagenda import config

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'


def today_and_tomorrow(date):
    dto = datetime.datetime(date.year, date.month, date.day, 0, 0, 0)
    today = config.LOCAL_TZ.localize(dto)

    tomorrow = (today + datetime.timedelta(days=1)).astimezone(config.UTC)
    today = today.astimezone(config.UTC)
    return (today.isoformat(), tomorrow.isoformat())


# get_events is slightly modified from the stock Google example code.
def get_events(date, calendar='primary', max_events=5):
    """get_events returns the events for date from the primary calendar."""
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    (today, tomorrow) = today_and_tomorrow(date)
    events_result = service.events().list(calendarId=calendar, timeMin=today,
                                          timeMax=tomorrow,
                                          maxResults=max_events,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        return []

    event_list = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        event_list.append(Event(start, event['summary']))
    return event_list


class Event:
    """An Event is a single event that contains a what and a when."""
    def __init__(self, when, what):
        self.when = when
        self.what = what

    def string(self):
        return '+ ' + self.when + '\n  ' + self.what

    def text(self):
        try:
            when = datetime.datetime.strptime(self.when[:19],
                                              "%Y-%m-%dT%H:%M:%S")
            return ('At ' + str(when.hour) + ' ' + str(when.minute) +
                    ', ' + self.what)
        except ValueError:
            try:
                _ = datetime.datetime.strptime(self.when[:10], "%Y-%m-%d")
                return self.what
            except ValueError:
                return 'At ' + self.when + ', ' + self.what
