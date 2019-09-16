CalMet Specidications
================================================================================

Calendar Event Metrics

Command
--------------------------------------------------------------------------------

|                  コマンド                   |                 説明                 |                          例                          |
|:--------------------------------------------|:-------------------------------------|:-----------------------------------------------------|
| list                                        | カレンダーの一覧を表示する           | calmet list                                          |
| fetch [\<options>] [\<calendar_id>] \<year> | データを取得してDBに保存する         | calmet fetch calendar@group.calendar.google.com 2019 |
| metrics [\<options>] \<year>                | データのメトリクスを計算して出力する | calmet metrics 2019                                  |


### list

カレンダー一覧を取得する。

```
$ python src/calmet.py list
id: calendar1@group.calendar.google.com, name: 勉強記録
id: calendar2@group.calendar.google.com, name: イベント
id: example@gmail.com, name: 予定
```


### fetch [\<options>] [\<calendar_id>] \<year>

指定のカレンダーの年に登録されているイベントをDBに保存する。
2回呼び出した場合は、前回取得した以降の新しいイベントのみを取得する。

#### --clean

取得済みのデータを削除してから再取得する。

#### --name=<calendar_name>

カレンダーIDの代わりにカレンダー名によってカレンダーを指定する。`--name`オプションを指定した場合、
`calendar_id`の指定は不要。

同名のカレンダーが複数存在する場合は、はじめにマッチしたカレンダーのイベントを取得する。

#### calenar_id

カレンダーのIDを指定する。指定したIDの指定した年のデータを保存する。


### metrics [\<options>] \<year>

指定年のデータのマトリクスを計算して出力する。

#### --type=<metrics_type>

`week`、`month`、`year`を指定する。出力はTSV形式。

`week`は1週間毎にイベント時間を合計して出力する。

```
$ python ./src/calmet.py metrics --type=week 2019
12-30   5.0
01-06   11.5
01-13   8.5
...(略)
09-01   25.0
09-08   16.5
total   339.5
```

`month`は1か月毎にイベント時間を合計して出力する。

```
$ python ./src/calmet.py metrics --type=month 2019
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

`year`は1年間のイベントを、イベント名毎にイベント時間を合計して出力する。

```
$ python ./src/calmet.py metrics --type=year 2019
CalMet  12.0
CodeceptJS      10.0
...(略)
『Software Design』     78.5
『日経Linux』   56.0
total   339.5
```


DB
--------------------------------------------------------------------------------

- SQLite 3
- events_{year}テーブルに年ごとにイベント情報を補完する
    - e.g. events_2019
- journalテーブルに各年ごとに情報を取得した期間や更新日を記録する


### journal table

- テーブル名: journal

テーブルのスキーマ

|   列    |  Type   |                     説明                      |              例               |
|:--------|:--------|:----------------------------------------------|:------------------------------|
| year    | INTEGER | プライマリキー。データの年                    | 2019                          |
| updated | TEXT    | テーブルを更新した日付。ISO8601形式           | 2019-09-07T20:44:12.345+09:00 |
| last    | TEXT    | テーブルに格納している最後の日付。ISO8601形式 | 2019-12-31T23:59:59.999+09:00 |
| api_ver | TEXT    | データを取得した際のAPIのバージョン           | v3                            |


### events table

- テーブル名: events_{year}
    - e.g. events_2019

テーブルのスキーマ

|      列       |  Type   |                    説明                     |                          例                          |
|:--------------|:--------|:--------------------------------------------|:-----------------------------------------------------|
| id            | INTEGER | プライマリキー。Calendar APIが返すeventのID | abcdefghijklmnopqrstuvwxyz                           |
| calendar_id   | TEXT    | カレンダーのID                              | abcdefghijklmnopqrstuvwxyz@group.calendar.google.com |
| calendar_name | TEXT    | カレンダーの名前                            | 01-勉強記録                                          |
| name          | TEXT    | イベント名                                  | 『Software Design』                                  |
| description   | TEXT    | イベントの説明文                            | vol:201909\nread:20                                  |
| start         | TEXT    | 開始日時。ISO8601形式                       | 2019-09-07T20:00:00.000+09:00                        |
| end           | TEXT    | 終了日時。ISO8601形式                       | 2019-09-07T21:00:00.00+09:00                         |
| minutes       | INTEGER | イベント時間。単位は「分」                  | 60                                                   |
| raw           | TEXT    | APIが返した生のデータ                       | {{"attachments": [...}                               |


参考
--------------------------------------------------------------------------------

- [Google Calendar API](https://developers.google.com/calendar/?hl=ja)
- [Calendar API PyDoc](https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/?hl=ja)
- [Calendar API Reference](https://developers.google.com/calendar/v3/reference/?hl=ja)
