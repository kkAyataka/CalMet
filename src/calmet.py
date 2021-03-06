# Copyright 2019 kkAyataka
#
# Distributed under the MIT License.
# https://opensource.org/licenses/MIT

import argparse
import datetime
import pickle
import os.path
from list_cmd import list_cmd
from metrics_cmd import metrics_cmd
from fetch_cmd import fetch_cmd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def def_cmd():
    p = argparse.ArgumentParser(description='Calendar Event Metrics')
    subp = p.add_subparsers(help='Commands')

    # list
    fetch = subp.add_parser('list', help='list calendars')
    fetch.set_defaults(func=list_cmd)

    # fetch
    fetch = subp.add_parser('fetch', help='fetch events data')
    fetch.add_argument('--clean', action='store_true', help='Delete all fetched data')
    fetch.add_argument('--name', type=str, dest='calendar_name', help='Specify calendar by name')
    fetch.add_argument('--id', type=str, dest='calendar_id', help='calendar id')
    fetch.add_argument('year', type=int, help='target year')
    fetch.set_defaults(func=fetch_cmd)

    # metrics
    metrics = subp.add_parser('metrics', help='calculate metrics data')
    metrics.add_argument('-t', '--type', choices=['week', 'month', 'year'], type=str, help="week, month or name")
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

if __name__ == '__main__':
    main()
