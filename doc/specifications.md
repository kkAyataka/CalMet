CalMet Specidications
================================================================================

Calendar Event Metrics

Command
--------------------------------------------------------------------------------

コマンド

|          コマンド          |                 説明                 |           例           |
|:---------------------------|:-------------------------------------|:-----------------------|
| fetch list                 | カレンダーの一覧を表示する           | calmet list            |
| fetch [\<options>] \<year>   | データを取得してDBに保存する         | calmet fetch 2019      |
| metrics [\<options>] \<year> | データのメトリクスを計算して出力する | calmet metrics -m 2019 |

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
| first   | TEXT    | テーブルに格納している最初の日付。ISO8601形式 | 2019-01-01T00:00:00.000+09:00 |
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
