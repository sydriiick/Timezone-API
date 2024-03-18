# Timezone API Script

This script populates a SQLite database with timezone information obtained from the TimezoneDB API.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- Required Python packages (install via `pip install -r requirements.txt`)
- TimezoneDB API key (obtain from [TimezoneDB](https://timezonedb.com/))

## Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/sydriiick/Timezone-API.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd timezone-database-population
    ```

3. **Install required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Create a SQLite database:**

    - Open a terminal or command prompt.
    - Navigate to the project directory.
    - Run the following command to create an empty SQLite database file named `timezone_db.sqlite`:

        ```bash
        sqlite3 timezone_db.sqlite
        ```

5. **Create the necessary tables:**

    - Once in the SQLite shell, copy and paste the following SQL commands located in the file `sqlite.sql`:
      
        ```sql
        CREATE TABLE IF NOT EXISTS TZDB_TIMEZONES (
            country_code VARCHAR(2) NOT NULL,
            country_name VARCHAR(100) NOT NULL,
            zone_name VARCHAR(100) PRIMARY KEY NOT NULL,
            gmtoffset NUMERIC,
            import_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS TZDB_ZONE_DETAILS (
            country_code VARCHAR(2) NOT NULL,
            country_name VARCHAR(100) NOT NULL,
            zone_name VARCHAR(100) NOT NULL,
            gmtoffset NUMERIC NOT NULL,
            dst NUMERIC NOT NULL,
            zone_start NUMERIC NOT NULL,
            zone_end NUMERIC NOT NULL,
            import_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (zone_name, zone_start, zone_end)
        );
        
        CREATE TABLE IF NOT EXISTS TZDB_ERROR_LOG (
            import_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            error_message VARCHAR(1000) NOT NULL
        );
        ```

6. **Obtain a TimezoneDB API key:**

    - Sign up for an account on [TimezoneDB](https://timezonedb.com/).
    - Once logged in, obtain your API key.

7. **Update the configuration:**

    - Open the `config.py` file.
    - Replace `"your_api_key_here"` with your TimezoneDB API key:

        ```python
        API_KEY = "your_api_key_here"
        ```

## Running the Script

1. **Open a terminal or command prompt.**

2. **Navigate to the project directory.**

3. **Run the script using Python:**

    ```bash
    python timezone.py
    ```

4. **The script will fetch timezone data from the TimezoneDB API and populate the SQLite database.**

## Notes

- Ensure your TimezoneDB API key is kept confidential and not shared publicly.
