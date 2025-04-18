import pandas as pd
import json

def lambda_handler(event, context):
    try:
        # Create pandas data frame using the url of the S3 Bucket.
        # With the s3fs extension, Pandas will use it to accept URLS with a "s3://" prefix.
        # s3fs builds on top of boto3 and will use it to pass ~/.aws/credentials to authenticate
        df = pd.read_csv("s3://raft-project-s3-bucket/flightlist_20190101_20190131.csv", low_memory=False)

        # row count starts at index 0 so add a 1
        row_count = df.index.max() + 1
        last_transponder_seen_at = df.lastseen.max()
        most_popular_destination = df.destination.value_counts().idxmax()
        count_of_unique_transponders = df.icao24.nunique()

        result = pd.DataFrame({'row_count': [row_count],
                               'last_transponder_seen_at': [last_transponder_seen_at],
                               'most_popular_destination': [most_popular_destination],
                               'count_of_unique_transponders': [count_of_unique_transponders]
                               })
        

        print(result)
        # Store Dataframe as a dict in a variable
        json_result = result.to_dict(orient='index')

        # Return json output of the Dataframe dictionary
        return {
        "statusCode": 200,
        "body": json.dumps(
            json_result
        )
    }

    except Exception as e:
        print(f"S3 connection failed due to {e}")