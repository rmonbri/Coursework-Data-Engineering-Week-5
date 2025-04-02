# pylint: disable = no-member
"""Import data to database"""
import os
import csv
from dotenv import load_dotenv
import pymssql
import pandas as pd

DATA_PATH = "./data/clean-plant-measurements.csv"


def get_connection_to_db() -> pymssql.Connection:
    """Gets a pymssql connection to the short term MS SQL short-term DB"""
    load_dotenv()
    return pymssql.connect(host=os.getenv("DB_HOST"),
                           database=os.getenv("DB_NAME"),
                           user=os.getenv("DB_USERNAME"),
                           password=os.getenv("DB_PASSWORD"),
                           port=os.getenv("DB_PORT"))


def get_measurements_from_csv(path: str = DATA_PATH) -> list[dict]:
    """Gets transformed and validated measurements 
    from data/clean-plant-measurements.csv unless a different path is specified"""
    with open(path, "r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        return [tuple(row) for row in csv_reader]


def get_measurements_from_df(data: pd.DataFrame) -> list[tuple]:

    return [tuple(row) for row in data.itertuples(index=False, name=None)]


def upload_many_rows(rows: list[tuple], conn) -> None:
    """Uploads a single measurement row to the database for the specified connection."""
    cur = conn.cursor()
    sql = """
        INSERT into measurement
        (plant_id, temperature, moisture, last_watered, measurement_time)
        VALUES
        (%s, %s, %s, %s, %s);
        """
    cur.executemany(sql, rows)
    conn.commit()


def ingress_measurements_to_db(measurements: list[tuple]) -> None:
    """Ingresses given measurement data into the short-term db"""
    conn = get_connection_to_db()
    upload_many_rows(measurements, conn)
    conn.close()


if __name__ == "__main__":
    plant_measurements = get_measurements_from_csv()
    ingress_measurements_to_db(plant_measurements)
