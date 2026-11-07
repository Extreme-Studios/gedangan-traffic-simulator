"""Lazy 2026 evidence-coverage view, not fabricated traffic records."""
import sqlite3
from .recovery_data import DB,initialize
from .recovery_common import *
def main():
 initialize()
 with sqlite3.connect(DB)as c:
  c.executescript('''CREATE VIEW IF NOT EXISTS target_calendar_2026 AS
WITH RECURSIVE dates(d) AS (VALUES('2026-08-01') UNION ALL SELECT date(d,'+1 day') FROM dates WHERE d<'2026-10-31'), slots(n) AS (VALUES(0) UNION ALL SELECT n+1 FROM slots WHERE n<95)
SELECT d AS date,CASE WHEN strftime('%w',d) IN ('0','6') THEN 'WEEKEND' ELSE 'WEEKDAY' END AS day_type,
printf('%02d:%02d',(n*15)/60,(n*15)%60) AS start_wib,'+07:00' AS utc_offset,900 AS interval_s,
CASE WHEN EXISTS(SELECT 1 FROM evidence e WHERE e.date=d AND e.start_wib=printf('%02d:%02d',(n*15)/60,(n*15)%60) AND e.status='OBSERVED' AND e.direction<>'UNSPECIFIED' AND e.interval_s=900) THEN 'OBSERVED' ELSE 'MISSING' END AS directional_count_status
FROM dates CROSS JOIN slots;''')
  counts=dict(c.execute('SELECT directional_count_status,count(*) FROM target_calendar_2026 GROUP BY directional_count_status'));rows=[dict(zip(['date','day_type','start_wib','utc_offset','interval_s','directional_count_status'],r))for r in c.execute("SELECT * FROM target_calendar_2026 WHERE start_wib IN ('07:00','17:00') LIMIT 12")]
 save(DOC/'target-coverage-view.json',{'sqlite_view':'target_calendar_2026','days':92,'quarter_hour_slots':92*96,'counts':counts,'examples':rows,'interpretation':'MISSING view rows are availability statements, not zero-volume observations. View is computed lazily and stores no invented historical counts.'});print(counts)
if __name__=='__main__':main()
