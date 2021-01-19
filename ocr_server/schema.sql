-- I think this table is extraneous and unused

DROP TABLE IF EXISTS dim_events;
CREATE TABLE dim_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date DATETIME,
  duration REAL,
  event_name TEXT
 );
