# Copyright 2019 kkAyataka
#
# Distributed under the MIT License.
# https://opensource.org/licenses/MIT

import datetime
import calmet_db
from calmet_db import JST
from calendar_api_service import build_service

def get_today():
    now = datetime.datetime.now()
    return datetime.datetime(now.year, now.month, now.day, tzinfo=JST())

def get_journal(db, year):
    journal = db.load_journal(year)

    today = get_today()

    if journal == None:
        first = datetime.datetime(year, 1, 1, 0, 0, 0, tzinfo=JST())
        last = datetime.datetime(year, 1, 1, 0, 0, 0, tzinfo=JST())
        journal = calmet_db.Journal(year, today, first, last)

    return journal

def fetch_events(calendar_id, last):
    timeMax = datetime.datetime(last.year, 12, 31, 23, 59, 59, tzinfo=JST()).isoformat()

    service = build_service()

    raw_events = []

    # get calendar info
    calendar = service.calendarList().get(calendarId=calendar_id).execute()

    # get events
    pageToken = None
    while True:
        res = service.events().list(
            calendarId=calendar_id,
            timeMin=last.isoformat(),
            timeMax=timeMax,
            singleEvents=True,
            orderBy='startTime',
            #maxResults=100,
            pageToken=pageToken
            ).execute()

        raw_events = raw_events + res.get('items', [])

        if 'nextPageToken' in res:
            pageToken = res['nextPageToken']
        else:
            break

    events = []
    for e in raw_events:
        events.append(calmet_db.Event.from_api_result_item(calendar_id, calendar['summary'], e))

    return events

def fetch_cmd(args):
    # get args
    calendar_id = args.calendar_id
    year = args.year

    # initialize
    db = calmet_db.CalMetDB()
    db.open()

    # get current db state
    journal = get_journal(db, year)

    # fetch events
    events = fetch_events(calendar_id, journal.last)

    # save
    db.save_events(year, events)

    if len(events) > 0:
        journal.updated = get_today()
        journal.last =  events[-1].start
        db.save_journal(journal)

    for e in events:
        print(e.name, e.minutes)

    # cleanup
    db.close()
