import argparse
import datetime
import pickle
import os.path
from list_cmd import list_cmd
from fetch_cmd import fetch_cmd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def metrics_cmd(args):
    print(args)

def def_cmd():
    p = argparse.ArgumentParser(description='Calendar Event Metrics')
    subp = p.add_subparsers(help='Commands')

    # list
    fetch = subp.add_parser('list', help='list calendars')
    fetch.set_defaults(func=list_cmd)

    # fetch
    fetch = subp.add_parser('fetch', help='fetch events data')
    fetch.add_argument('calendar_id', metavar="calendar_id", type=str, help='calendar id')
    fetch.add_argument('year', metavar="year", type=int, help='target year')
    fetch.set_defaults(func=fetch_cmd)

    # metrics
    metrics = subp.add_parser('metrics', help='calculate metrics data')
    metrics.add_argument('-m', '--month', type=str, help="metrics unit")
    metrics.add_argument('year', metavar="target year", type=int, help="target year")
    metrics.set_defaults(func=metrics_cmd)

    args = p.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        p.print_help()
        exit(-1)

def main():
    def_cmd()
    return

    creds = None
    # read token
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # get credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call API

    calendar_list_res = service.calendarList().list().execute()
    calendar_list = calendar_list_res.get('items')

    from_date = datetime.datetime(2019, 9, 1).isoformat() + 'Z'

    events_result = service.events().list(
        calendarId='ukpov7g2h96tjts3hhiatcge98@group.calendar.google.com',
        timeMin=from_date,
        maxResults=10,
        singleEvents=True,
        orderBy='startTime'
        ).execute()



    events = events_result.get('items', [])

    if not events:
        print('No events')

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

if __name__ == '__main__':
    main()
