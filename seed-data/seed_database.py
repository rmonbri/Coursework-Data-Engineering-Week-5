import os
import csv
import pymssql
from dotenv import load_dotenv


def get_connection_to_db() -> pymssql.connection:
    '''Gets a pymssql connection to the short term MS SQL short-term DB'''
    load_dotenv()
    return pymssql.connect(host=os.getenv('DB_HOST'),
                           database=os.getenv('DB_NAME'),
                           user=os.getenv('DB_USERNAME'),
                           password=os.getenv('DB_PASSWORD'),
                           port=os.getenv('DB_PORT'))


def get_data_from_file(path: str):
    '''Loads file'''
    with open(path, 'r') as file:
        csv_reader = csv.reader(file)
        return [tuple(row) for row in csv_reader]


def add_data_to_database(data):
    for i in data[0]:
        print(i)


if __name__ == "__main__":
    botanist_data = get_data_from_file("botanist.csv")
    add_data_to_database(botanist_data)


# sqlcmd -S c16-louis-db.c57vkec7dkkx.eu-west-2.rds.amazonaws.com -U louis_admin -P pd8W2rPBam4a
