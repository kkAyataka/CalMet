CalMet
======

Calculate event metrics of the Google Calendar


Build and Run
-------------

1. Turn on the Google Calendar API by [Official Guide](https://developers.google.com/calendar/quickstart/python?hl=ja)
2. Download credentials.json and locate at project root directory
2. Install dependent libraries
    - `pip install -r pip-requirements.txt`
3. Run calmet
    - `python src/calmet.py list`
    - `python src/calmet.py fetch calendar@group.calendar.google.com 2019`
    - `python src/calmet.py metrics 2019`


Fetch event data and Get metrics
--------------------------------

### 1. Get calendar list

```
$ python src/calmet.py list
id: calendar@group.calendar.google.com, name: Schedule
```

### 2. Fetch event data and save to db

```
$ python src/calmet.py fetch calendar@group.calendar.google.com 2019
```

### 3. Get metrics

```
$ python src/calmet.py metrics --type=month 2019
01      45.5
02      66.0
03      33.0
04      9.0
05      26.0
06      9.5
07      47.5
08      61.5
09      41.5
total   339.5
```


License
-------

[MIT License](LICENSE.txt)
