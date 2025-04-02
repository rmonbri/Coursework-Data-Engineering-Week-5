'''This script detects anomalies in the last n (SPECIFY) measurements from the plant readers'''
from dotenv import load_dotenv
import pymssql
import pandas as pd

def get_connection() -> pymssql.Connection:
    load_dotenv()
    return pymssql.connect(host=os.getenv("DB_HOST"),
                           database=os.getenv("DB_NAME"),
                           user=os.getenv("DB_USERNAME"),
                           password=os.getenv("DB_PASSWORD"),
                           port=os.getenv("DB_PORT"))

def get_last_n_measurements(n:int) -> pd.DataFrame:
    ''''''
    print('a')



if __name__ == '__main__':
    print('a')