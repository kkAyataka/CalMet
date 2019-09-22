# Copyright 2019 kkAyataka
#
# Distributed under the MIT License.
# https://opensource.org/licenses/MIT

import calmet_db

def metrics_cmd(args):
    # args
    mettype = args.type
    year = args.year

    # initialize
    db = calmet_db.CalMetDB()
    db.open()

    if mettype == 'week':
        metrics = db.get_per_week_metrics(year)
    elif mettype == 'month':
        metrics = db.get_per_month_metrics(year)
    else:
        metrics = db.get_per_name_metrics(year)

    sum_hours = 0
    for m in metrics:
        sum_hours += m[1]

    for m in metrics:
        print(f'{m[0]}\t{m[1]}')

    print(f'total\t{sum_hours}')

    # cleanup
    db.close()
