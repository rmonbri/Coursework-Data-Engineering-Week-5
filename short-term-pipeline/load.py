from dotenv import load_dotenv
import os
import psycopg2
import pandas as pd

DATA_PATH = 'a'


def get_connection_to_db() -> psycopg2.connection:
    '''Gets a psycopg2 connection to the short term MS SQL short-term DB'''
    load_dotenv()
    return psycopg2.connect(host=os.getenv('DB_HOST'),
                            database=os.getenv('DB_NAME'),
                            user=os.getenv('DB_USERNAME'),
                            password=os.getenv('DB_PASSWORD'),
                            port=os.getenv('DB_PORT'))


def create_temp_table(conn: psycopg2.connection) -> None:
    '''creates temporary table to upload the measurements batch data to the database'''
    sql_create_tmp_table = """
                DROP TABLE IF EXISTS tmp_table;
                CREATE TABLE tmp_table (
                at TIMESTAMPTZ,
                site smallint,
                val float,
                type float
                );
              """


def get_measurements(path: str = DATA_PATH) -> pd.DataFrame | dict | list[dict]:
    '''Gets transformed and validated measurements from  data/(something.csv)'''
    # TODO(FEATURE): Waiting on transformation data output path (i could just ask tbh)
    pass


def ingress_measurements_to_db():
    '''Ingresses given measurement data into the short-term db'''
    pass


def delete_ingressed_data_files() -> None:
    '''Deletes the files where the data was ingressed from'''
    pass


if __name__ == '__main__':
    print('a')
