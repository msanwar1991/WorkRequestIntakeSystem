import sqlite3
import json
from datetime import datetime

# Function to convert ISO 8601 format to SQLite datetime format
def convert_iso_to_datetime(iso_str):
    return datetime.fromisoformat(iso_str.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M:%S.%f")

# Define connection to the SQLite database
db_filename = 'work_requests.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_filename)

# Create a cursor object
cur = conn.cursor()

# Define the SQL statement to create the table
create_table_sql = """
DROP TABLE IF EXISTS work_requests;
CREATE TABLE work_requests (
    id INTEGER PRIMARY KEY,
    request_detail TEXT NOT NULL,
    equipment_name TEXT NOT NULL,
    station_name TEXT NOT NULL,
    date_condition_observed DATETIME NOT NULL,
    spare_part_required BOOLEAN NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

# Execute the SQL statement
cur.executescript(create_table_sql)

# Load JSON data from the file
with open('other/seed_data.json', 'r') as file:
    data = json.load(file)

# Define the SQL statement for inserting data
insert_sql = """
INSERT INTO work_requests (
    id,
    request_detail,
    equipment_name,
    station_name,
    date_condition_observed,
    spare_part_required,
    created_at
) VALUES (?, ?, ?, ?, ?, ?, ?);
"""

# Insert each entry from the JSON data into the work_requests table
for entry in data:
    cur.execute(insert_sql, (
        entry['id'],
        entry['request_detail'],
        entry['equipment_name'],
        entry['station_name'],
        convert_iso_to_datetime(entry['date_condition_observed']),
        entry['spare_part_required'],
        convert_iso_to_datetime(entry['created_at'])
    ))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database initialized and data imported successfully.")