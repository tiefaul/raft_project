import psycopg2
import os
import boto3

endpoint = os.environ['ENDPOINT']
port = os.environ['PORT']
db_name = os.environ['DB_NAME']
db_user_name = os.environ['DB_USER_NAME']
password = os.environ['PASSWORD']

def lambda_handler(event, context):
    '''
# For more security. Use boto3 to create an (optional) token and use it to pass authentication into the Postgresql database.

# Get the credentials from your .aws/credentials file
session = boto3.Session(profile_name='default')
client = session.client('rds')

# Generate token and pass it into the psycopg connection's password field
token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)
'''

    try:
        # Connect to the database.
        conn = psycopg2.connect(host=endpoint, port=port, database=db_name, user=db_user_name, password=password)
        cur = conn.cursor()
    
        # Create tables for the data.
        print("Creating tables for the data....")
        cur.execute("CREATE TABLE raftproject (callsign varchar(255), number varchar(255), icao24 varchar(255), registration varchar(255), typecode varchar(255), origin varchar(255), destination varchar(255), firstseen varchar(255), lastseen varchar(255), day varchar(255), latitude_1 varchar(255), longitude_1 varchar(255), altitude_1 varchar(255), latitude_2 varchar(255), longitude_2 varchar(255), altitude_2 varchar(255));")

        # Insert S3 data.
        print("Inserting S3 bucket data....")

        # Get s3_uri
        cur.execute("""SELECT aws_commons.create_s3_uri(
                    'raft-project-s3-bucket',
                    'flightlist_20190101_20190131.csv',
                    'us-east-1'
                    ) AS s3_uri;""")
    
        s3_uri = cur.fetchone()[0] # type: ignore

        # Execute Postgresql S3 bucket extenstion to import data to database
        cur.execute(f"""SELECT aws_s3.table_import_from_s3(
                    'raftproject',
                    '',
                    '(FORMAT csv, DELIMITER '','', HEADER true, NULL '''')',
                    '{s3_uri}'
                    );""")

        # Save config and close
        print("S3 data import complete. Closing session")
        conn.commit()
        cur.close()
        conn.close()

        return {
            "statusCode": 200,
            "message": "S3 bucket data successfully imported!"
        }

    # Create exception if connection fails.
    except Exception as e:
        print(f"Database connection failed due to {e}")