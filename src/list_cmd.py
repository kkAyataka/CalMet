# Copyright 2019 kkAyataka
#
# Distributed under the MIT License.
# https://opensource.org/licenses/MIT

import datetime
from calendar_api_service import build_service

def list_cmd(args):
    role = 'owner'
    service = build_service()

    calendar_list_res = service.calendarList().list(minAccessRole=role).execute()
    calendar_list = calendar_list_res.get('items')

    for c in calendar_list:
        print(f'id: {c["id"]}, name: {c["summary"]}')

