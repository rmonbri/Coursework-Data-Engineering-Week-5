"""File to read csvs and seed the database"""
import os
import csv
import pymssql
from dotenv import load_dotenv

BOTANIST_SQL = """
        INSERT into botanist
        (botanist_number, botanist_email, botanist_name)
        VALUES
        (%s, %s, %s);
        """

ORIGIN_SQL = """
        INSERT into origin
        (latitude, longitude, locality, country_code, timezone)
        VALUES
        (%s, %s, %s, %s, %s);
        """

PLANT_TYPE_SQL = """
        INSERT into plant_type
        (plant_name, scientific_name)
        VALUES
        (%s, %s);
        """

PLANT_SQL = """
        INSERT into plant
        (plant_id, botanist_id, location_id, plant_type_id)
        VALUES
        (%s, %s, %s, %s);
        """


def get_connection_to_db() -> "pymssql.connection":
    '''Gets a pymssql connection to the short term MS SQL short-term DB'''
    load_dotenv('.env.prod')
    return pymssql.connect(host=os.getenv('DB_HOST'),
                           database=os.getenv('DB_NAME'),
                           user=os.getenv('DB_USERNAME'),
                           password=os.getenv('DB_PASSWORD'),
                           port=os.getenv('DB_PORT'))


def get_data_from_file(path: str):
    '''Loads file'''
    with open(path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        return [tuple(row) for row in csv_reader]


def add_data_to_database(data, sql_command: str):
    """Create connection, Pass data and SQL to upload function"""
    db_conn = get_connection_to_db()
    upload_many_rows(data, db_conn, sql_command)
    db_conn.close()


def upload_many_rows(rows: list[tuple], conn: "pymssql.Connection", sql_command: str) -> None:
    """Uploads a single measurement row to the database for the specified connection."""
    cur = conn.cursor()
    cur.executemany(sql_command, rows)
    conn.commit()


if __name__ == "__main__":
    botanist_data = get_data_from_file("botanist.csv")
    origin_data = get_data_from_file("origin.csv")
    plant_type = get_data_from_file("plant_type.csv")
    plant_data = get_data_from_file("plant_id.csv")

    add_data_to_database(botanist_data, BOTANIST_SQL)
    add_data_to_database(origin_data, ORIGIN_SQL)
    add_data_to_database(plant_type, PLANT_TYPE_SQL)
    add_data_to_database(plant_data, PLANT_SQL)


# sqlcmd -S c16-louis-db.c57vkec7dkkx.eu-west-2.rds.amazonaws.com -U louis_admin -P pd8W2rPBam4a
