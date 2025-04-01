import os
import csv
from dotenv import load_dotenv
from shutil import rmtree
import pymssql

DATA_PATH = './data/clean-plant-measurements.csv'


def get_connection_to_db() -> pymssql.connection:
    '''Gets a pymssql connection to the short term MS SQL short-term DB'''
    load_dotenv()
    return pymssql.connect(host=os.getenv('DB_HOST'),
                           database=os.getenv('DB_NAME'),
                           user=os.getenv('DB_USERNAME'),
                           password=os.getenv('DB_PASSWORD'),
                           port=os.getenv('DB_PORT'))


def get_measurements(path: str = DATA_PATH) -> list[dict]:
    '''Gets transformed and validated measurements 
    from data/clean-plant-measurements.csv unless a different path is specified'''
    with open(path, 'r') as file:
        csv_reader = csv.reader(file)
        return [tuple(row) for row in csv_reader]


def upload_row(row: tuple, conn: pymssql.connection) -> None:
    '''Uploads a single measurement row to the database for the specified connection.'''
    cur = conn.cursor()
    sql = '''
        INSERT into measurement
        (plant_id, measurement_time, last_watered, moisture, temperature)
        VALUES
        (%s, %s, %s, %s, %s);
        '''
    cur.execute(sql, row)
    cur.commit()


def ingress_measurements_to_db(measurements: list[tuple]) -> None:
    '''Ingresses given measurement data into the short-term db'''
    conn = get_connection_to_db()
    for measurement_row in measurements:
        upload_row(measurement_row, conn)


def delete_ingressed_data_files(path: str = DATA_PATH) -> None:
    '''Deletes the file where the data was ingressed from'''
    if os.path.exists(path):
        os.remove(path)
    else:
        print("The file does not exist")


if __name__ == '__main__':
    measurements = get_measurements()
    ingress_measurements_to_db(measurements)
    delete_ingressed_data_files()
