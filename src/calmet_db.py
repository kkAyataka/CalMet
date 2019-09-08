import datetime
import sqlite3

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
    calendar_id = None
    calendar_name = None
    event_name = None
    description = None
    start = None
    end = None
    minutes = None
    raw = None

    @staticmethod
    def from_api_result_item(calendar_id, calendar_name, item):
        return Event(
            calendar_id,
            calendar_name,
            item.get('summary', ''),
            item.get('description', ''),
            datetime.datetime.fromisoformat(item['start']['dateTime']),
            datetime.datetime.fromisoformat(item['end']['dateTime']),
            item)

    def __init__(self, calendar_id, calendar_name, event_name, description, start, end, raw):
        self.calendar_id = calendar_id
        self.calendar_name = calendar_name
        self.event_name = event_name
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

    def get_journal(self, year):
        self.connection.execute(
            f'SELECT * from journal WHERE year = {year}')

        j = self.connection.cursor().fetchone()

        if j != None:
            return Journal(
                j.year,
                datetime.datetime.fromisoformat(j.updated),
                datetime.datetime.fromisoformat(j.first),
                datetime.datetime.fromisoformat(j.last),
                j.app_ver)
        else:
            return None

    def set_journal(self, journal:Journal):
        self.connection.execute(
            f'INSERT OR REPLACE INTO journal VALUES('
            f'  {journal.year},'
            f'  {journal.updated.isoformat()},'
            f'  {journal.first.isoformat()},'
            f'  {journal.last.isoformat()},'
            f'  {journal.app_ver}'
            f')')

        self.connection.commit()

