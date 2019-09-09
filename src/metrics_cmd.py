import calmet_db

def metrics_cmd(args):
    # args
    year = args.year

    # initialize
    db = calmet_db.CalMetDB()
    db.open()

    metrics = db.get_metrics(year)

    sum_hours = 0
    for m in metrics:
        sum_hours += m[1]

    for m in metrics:
        print(f'{m[0]}\t{m[1]}')

    print(f'total\t{sum_hours}')

    # cleanup
    db.close()
