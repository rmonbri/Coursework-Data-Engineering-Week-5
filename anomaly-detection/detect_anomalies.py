'''This script detects anomalies in the last n (SPECIFY) measurements from the plant readers'''
import os
from dotenv import load_dotenv
import pymssql
import pandas as pd
from scipy.stats import zscore

def get_connection_to_db() -> pymssql.Connection:
    """Gets a pymssql connection to the short term MS SQL short-term DB"""
    load_dotenv()
    return pymssql.connect(host=os.getenv("DB_HOST"),
                           database=os.getenv("DB_NAME"),
                           user=os.getenv("DB_USERNAME"),
                           password=os.getenv("DB_PASSWORD"),
                           port=os.getenv("DB_PORT"),)


def get_last_n_measurements(n:int) -> pd.DataFrame:
    '''Gets a dataframe with the last n measurement batches from the short-term database'''
    try:
        n = n*50 # This assumes that we're logging null values when there are no responses. This should work since each batch of 50 measurements will be spaced out by 1 min, but maybe we need a more robust way of doing this? 
        conn = get_connection_to_db()
        sql = f'''
              SELECT TOP {n} 
              * 
              FROM measurement
              ORDER BY measurement_type DESC;
              '''
        df = pd.read_sql(sql,conn)
        return df
    finally:
        conn.close()
    
def add_zscore_columns(measurements:pd.DataFrame) -> pd.Dataframe:
    '''Returns a measurements df with added zscore columns for moisture and temperature'''
    measurements[['moisture_zscore','temperature_zscore']] = measurements[['moisture','temperature']].apply(zscore)
    return measurements

def get_outliers_by_zscore(measurements:pd.DataFrame,zscore_threshold:float =2.5) -> pd.DataFrame:
    '''Returns a dataframe of outliers whose zscores is greater than 2.5 unless specified otherwise.'''
    condition = measurements[['moisture_zscore','temperature_zscore']].abs() < zscore_threshold
    return measurements[condition]

def get_outlier_count_per_plant() -> dict:
    pass

def alert_inconsistency() -> dict:
    pass


if __name__ == '__main__':
    get_connection_to_db()
    print(get_last_n_measurements(10))