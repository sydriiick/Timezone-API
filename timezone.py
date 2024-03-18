import sqlite3
import requests
import time
from datetime import datetime
import config


def db_connection():
    """Establishes a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(config.DB_FILE)
        return conn
    except sqlite3.Error as e:
        print("Error connecting to the database:", e)
        return None


def log_error(conn, error_message):
    """Logs errors into the TZDB_ERROR_LOG table."""
    try:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO TZDB_ERROR_LOG (error_date, error_message) VALUES (?,?)''',
                       (datetime.now(), error_message,))
        conn.commit()
    except sqlite3.Error as e:
        print("Error logging error message:", e)


def populate_timezones_table(conn):
    """Populates the TZDB_TIMEZONES table with data from the TimezoneDB API."""
    try:
        cursor = conn.cursor()

        # Deleting the TZDB_TIMEZONES table before populating it.
        cursor.execute("DELETE FROM TZDB_TIMEZONES")

        params = {"key": config.API_KEY, 'format': 'json'}
        response = requests.get(config.LIST_URL, params=params)
        response.raise_for_status()
        timezones = response.json()["zones"]

        for timezone in timezones:
            
            details = (timezone["countryCode"], timezone["countryName"], 
                        timezone["zoneName"], timezone["gmtOffset"], datetime.now())
            
            # Insert data into TZDB_TIMEZONES
            cursor.execute('''INSERT INTO TZDB_TIMEZONES (country_code, 
                            country_name,zone_name, gmtoffset, import_date)
                            VALUES (?, ?, ?, ?, ?)''', details)
        conn.commit()
    except (requests.RequestException, sqlite3.Error) as e:
        log_error(conn, "Error populating TZDB_TIMEZONES table: " + str(e))


def populate_zone_details_table(conn):
    """Populates the TZDB_ZONE_DETAILS table with data from the TimezoneDB API."""
    try:
        cursor = conn.cursor()

        # Create a temporary table for storing zone details
        cursor.execute('''CREATE TEMP TABLE IF NOT EXISTS temp_zone_details 
                          AS SELECT * FROM TZDB_ZONE_DETAILS''')

        # Fetch all zone names from TZDB_TIMEZONES
        cursor.execute("SELECT zone_name from TZDB_TIMEZONES")
        zones = cursor.fetchall()

        for zone in zones:
            
            params= {"key": config.API_KEY, "format": "json", "by": "zone", "zone": zone}
            response = requests.get(config.ZONE_URL, params=params)
            response.raise_for_status()
            detail = response.json()

            # If zoneEnd is not available, set it to 0
            if not detail['zoneEnd']:
                detail['zoneEnd'] = 0
            
            details = (detail["countryCode"], detail["countryName"], 
                       detail["zoneName"], detail["gmtOffset"], detail["dst"], 
                       detail["zoneStart"], detail["zoneEnd"], datetime.now())
            
            # Check if data for the zone already exists in TZDB_ZONE_DETAILS
            cursor.execute('''SELECT COUNT(*) FROM TZDB_ZONE_DETAILS 
                           WHERE zone_name = ?''', (zone[0],))
            existing_data = cursor.fetchone()[0]

            # If data doesn't exist, insert into the temporary table
            if existing_data == 0:
                cursor.execute('''INSERT INTO temp_zone_details 
                               (country_code, country_name, zone_name, gmtoffset, 
                               dst, zone_start, zone_end, import_date) 
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', details)
            
            # Adding 2 seconds deloy to avoid 429 Too Many Requests.
            time.sleep(2)
        # Insert data from temp table to TZDB_ZONE_DETAILS
        cursor.execute("INSERT INTO TZDB_ZONE_DETAILS SELECT * FROM temp_zone_details")
        
        conn.commit()
    except (requests.RequestException, sqlite3.Error) as e:
        log_error(conn, "Error populating TZDB_ZONE_DETAILS table: " + str(e))


def main():
    conn = db_connection()
    if conn:
        populate_timezones_table(conn)
        populate_zone_details_table(conn)
        conn.close()


if __name__ == "__main__":
    main()
