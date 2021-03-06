# Copyright 2019 kkAyataka
#
# Distributed under the MIT License.
# https://opensource.org/licenses/MIT

import datetime
import json
import sqlite3

def get_datetime(obj):
    string = ''
    if 'dateTime' in obj:
        string = obj['dateTime']
    elif 'date' in obj:
        string = obj['date']

    return datetime.datetime.fromisoformat(string)

class JST(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(hours=+9)
    def dst(self, dt):
        return datetime.timedelta()

class Journal:
    year = 2019
    updated = None
    first = None
    last = None
    api_ver = 'v3'

    def __init__(self, year:int, updated, first, last, api_ver:str='v3'):
        self.year = year
        self.updated = updated
        self.first = first
        self.last = last
        self.api_ver = 'v3'

class Event:
    id = None
    calendar_id = None
    calendar_name = None
    name = None
    description = None
    start = None
    end = None
    minutes = None
    raw = None

    @staticmethod
    def from_api_result_item(calendar_id, calendar_name, item):
        return Event(
            item['id'],
            calendar_id,
            calendar_name,
            item.get('summary', ''),
            item.get('description', ''),
            get_datetime(item['start']),
            get_datetime(item['end']),
            item)

    def __init__(self, id, calendar_id, calendar_name, event_name, description, start, end, raw):
        self.id = id
        self.calendar_id = calendar_id
        self.calendar_name = calendar_name
        self.name = event_name
        self.description = description
        self.start = start
        self.end = end
        self.minutes = (end - start).seconds / 60
        self.raw = raw

class CalMetDB:
    connection = None

    def open(self, path='calmet.db'):
        self.connection =  sqlite3.connect(path)
        # journal
        self.connection.execute(
            'CREATE TABLE IF NOT EXISTS journal ('
            '  year INTEGER NOT NULL PRIMARY KEY,'
            '  updated TEXT NOT NULL,'
            '  first TEXT NOT NULL,'
            '  last TEXT NOT NULL,'
            '  api_ver TEXT NOT NULL'
            ')')

        self.connection.commit()

    def close(self):
        self.connection.close()

    def load_journal(self, year):
        cursor = self.connection.cursor()
        cursor.execute(
            f'SELECT * from journal WHERE year = {year}')

        j = cursor.fetchone()

        if j != None:
            return Journal(
                j[0],
                datetime.datetime.fromisoformat(j[1]),
                datetime.datetime.fromisoformat(j[2]),
                datetime.datetime.fromisoformat(j[3]),
                j[4])
        else:
            return None

    def save_journal(self, journal:Journal):
        self.connection.execute(
            f'INSERT OR REPLACE INTO journal VALUES('
            f'  {journal.year},'
            f'  "{journal.updated.isoformat()}",'
            f'  "{journal.first.isoformat()}",'
            f'  "{journal.last.isoformat()}",'
            f'  "{journal.api_ver}"'
            f')')

        self.connection.commit()

    def clean_events(self, year):
        self.connection.execute(f'DELETE FROM journal WHERE year={year}')
        self.connection.execute(f'DROP TABLE IF EXISTS events_{year}')
        self.connection.commit()

    def save_events(self, year, events):
        # create table
        self.connection.execute(
            f'CREATE TABLE IF NOT EXISTS events_{year} ('
            f'  id TEXT NOT NULL PRIMARY KEY,'
            f'  calendar_id TEXT NOT NULL,'
            f'  calendar_name TEXT NOT NULL,'
            f'  name TEXT NOT NULL,'
            f'  description TEXT NOT NULL,'
            f'  start TEXT NOT NULL,'
            f'  end TEXT NOT NULL,'
            f'  minutes INTEGER NOT NULL,'
            f'  raw TEXT NOT NULL'
            f')')

        for e in events:
            self.connection.execute(
                f'INSERT OR REPLACE INTO events_{year} VALUES('
                f'  "{e.id}",'
                f'  "{e.calendar_id}",'
                f'  "{e.calendar_name}",'
                f'  "{e.name}",'
                f'  \'{e.description}\','
                f'  "{e.start.isoformat()}",'
                f'  "{e.end.isoformat()}",'
                f'  {e.minutes},'
                f'  \'{json.dumps(e.raw)}\''
                f')')

        self.connection.commit()

    def get_per_week_metrics(self, year):
        cursor = self.connection.cursor()
        cursor.execute(
            f'SELECT strftime("%m-%d", start, "weekday 6", "-6 days"), SUM(minutes)/60.0'
            f'  FROM events_{year} GROUP BY strftime("%W", start, "weekday 6")')

        return cursor.fetchall()


    def get_per_month_metrics(self, year):
        cursor = self.connection.cursor()
        cursor.execute(
            f'SELECT strftime("%m", start), SUM(minutes)/60.0 FROM events_{year} GROUP BY strftime("%m", start)')

        return cursor.fetchall()

    def get_per_name_metrics(self, year):
        cursor = self.connection.cursor()
        cursor.execute(
            f'SELECT name, SUM(minutes)/60.0 FROM events_{year} GROUP BY name')

        return cursor.fetchall()
