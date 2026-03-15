"""Load ferry ridership to Oracle"""

import csv
import oracledb
import os

# Initialize the database client
oracledb.init_oracle_client()

# Values to upload
values = []
# Open a the data file for reading
with open('ferry-ridership.csv') as data:
    reader = csv.reader(data)
    next(reader)
    for r in reader:
        values.append({
            'routeid': r[0],
            'routename': r[1],
            'ridership_date': r[2],
            'ridership': r[3]
        })

oracle_password = os.environ["ORACLE_PASSWORD"]

# Connect to the database
with oracledb.connect(user='USER1',
    password=oracle_password,
    dsn='gisy6021_high') as con:

    # Obtain a cursor for executing SQL 
    with con.cursor() as cursor:

        # Create a table
        cursor.execute("""
            create table ferry_ridership (
                routeid int,
                routename varchar2(50),
                ridership_date date,
                ridership int
            )
        """)

        # Execute the insert
        cursor.executemany("""
            insert into ferry_ridership
            values (
                :routeid,
                :routename,
                to_date(:ridership_date, 'YYYY-MM-DD'),
                :ridership
            )
        """, values)

        # Commit changes
        con.commit()
