"""Lambda Handler that moves old records to S3 Storage"""
# pylint: disable = no-member
import os
import io
import logging
from datetime import datetime, timedelta
import boto3
import pymssql
from dotenv import load_dotenv
import pandas as pd

load_dotenv('.env.prod')
BUCKET_NAME = os.getenv("BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


def enable_logging() -> None:
    """Enables logging at INFO level"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )


def connect_to_db() -> pymssql.Connection:
    """Create a connection to the database"""
    logging.info("Creating DB connection")
    return pymssql.connect(host=os.getenv("DB_HOST"),
                           database=os.getenv("DB_NAME"),
                           user=os.getenv("DB_USERNAME"),
                           password=os.getenv("DB_PASSWORD"),
                           port=os.getenv("DB_PORT"),
                           as_dict=True)


def get_old_data(cutoff_date: datetime) -> list[dict]:
    """Retrieve old records from the database"""
    db_conn = connect_to_db()
    db_cursor = db_conn.cursor()
    logging.info("Connected, retrieving old data...")

    db_cursor.execute("""SELECT *
    FROM measurement
    WHERE measurement_time < %s;""", cutoff_date)

    data = db_cursor.fetchall()
    db_cursor.close()
    db_conn.close()
    logging.info("Connection closed, data fetched.")
    return data


def generate_file(data: list[dict]) -> io.BytesIO:
    """Create DataFrame and create parquet file from that"""
    logging.info("Creating DataFrame")
    df = pd.DataFrame(data)
    logging.info("Saving data...")
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False)
    logging.info("Saved parquet to buffer")
    return buffer


def generate_key(date_time: datetime) -> str:
    """Generate a file key from date"""
    key = date_time.strftime("historical/%Y-%m/%d/measurements_%H.parquet")
    logging.info("Generated key string: %s", key)
    return key


def upload_data(key: str, buffered_data: io.BytesIO) -> dict:
    """Upload data from memory to bucket"""
    s3_client = boto3.client('s3')
    logging.info("Uploading data...")
    response = s3_client.put_object(Bucket=BUCKET_NAME,
                                    Key=key, Body=buffered_data.getvalue())
    logging.info("Uploading done")
    return response


def delete_old_data(cutoff_date: datetime):
    """Delete old rows from the database"""
    logging.info("Deleting old records from the database.")
    db_conn = connect_to_db()
    db_cursor = db_conn.cursor()

    db_cursor.execute("""SELECT COUNT(*) as Count
    FROM measurement
    WHERE measurement_time < %s;""", cutoff_date)

    rows = db_cursor.fetchone()
    db_cursor.close()
    db_conn.close()
    logging.info("Dropped %s rows", rows.get('Count'))


def handler(event, context):
    """Main handler function"""
    enable_logging()
    logging.info("Lambda Running - Event: %s", event)
    logging.info("Lambda Context passed: %s", context)

    cutoff_datetime = datetime.now() - timedelta(hours=24)
    cutoff_datetime = cutoff_datetime.replace(
        minute=0, second=0, microsecond=0)

    logging.info("Cutting off data older than: %s", cutoff_datetime)

    old_data = get_old_data(cutoff_datetime)
    if not old_data:
        logging.info("No data present... Exiting...")
        return {'status': 404}

    buffered_data = generate_file(old_data)
    key = generate_key(cutoff_datetime)
    response = upload_data(key, buffered_data)

    status = response.get('ResponseMetadata').get('HTTPStatusCode')
    logging.info("Recieved Status code: %s", status)

    if status != 200:
        logging.error("Error! - Status Code: %s", status)
        return {'status': status}

    delete_old_data(cutoff_datetime)
    return {'status': 200}


if __name__ == '__main__':
    handler(None, None)
