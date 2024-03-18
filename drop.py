import sqlite3

conn = sqlite3.connect('timezone_db.sqlite')

cursor = conn.cursor()

cursor.execute("DROP TABLE TZDB_TIMEZONES")
cursor.execute("DROP TABLE TZDB_ZONE_DETAILS")
cursor.execute("DROP TABLE TZDB_ERROR_LOG")

conn.commit()
conn.close()