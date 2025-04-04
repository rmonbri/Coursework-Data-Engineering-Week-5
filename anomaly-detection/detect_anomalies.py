'''This script detects anomalies in the last 15 measurements from the plant readers'''
import os
from datetime import datetime, timedelta
import pytz
from scipy.stats import zscore
from dotenv import load_dotenv
import pymssql
import pandas as pd


def get_connection_to_db() -> pymssql.Connection:
    """Gets a pymssql connection to the short term MS SQL short-term DB"""
    load_dotenv()
    return pymssql.connect(host=os.getenv("DB_HOST"),
                           database=os.getenv("DB_NAME"),
                           user=os.getenv("DB_USERNAME"),
                           password=os.getenv("DB_PASSWORD"),
                           port=os.getenv("DB_PORT"))


def get_time_n_minutes_ago(n: int) -> datetime:
    '''Gets a timestamp for n minutes ago '''
    # n will be specified later on based on data observations
    utc_now = datetime.now(pytz.utc)
    time = utc_now - timedelta(minutes=n)
    print(time)
    return time.strftime('%Y-%m-%d %H:%M:%S')


def get_sql_for_recent_measurements(n: int) -> str:
    '''Gets an sql query statement for the last n minutes of measurements'''''
    time = get_time_n_minutes_ago(n)
    sql = f'''
        SELECT plant_id,moisture,temperature
        FROM measurement
        WHERE measurement_time > '{time}'
        order by measurement_time desc
        '''
    return sql


def get_recent_measurements(n: int = 15) -> pd.DataFrame:
    '''Gets a dataframe with the last n measurement batches from the short-term database'''
    try:
        conn = get_connection_to_db()
        sql = get_sql_for_recent_measurements(n)
        df = pd.read_sql(sql, conn)
        return df
    finally:
        conn.close()


def add_zscore_columns(measurements: pd.DataFrame) -> pd.DataFrame:
    '''Returns a measurements df with added zscore columns for moisture and temperature'''
    measurements[['moisture_zscore', 'temperature_zscore']
                 ] = measurements[['moisture', 'temperature']].apply(zscore)
    return measurements


def get_outliers_by_zscore(measurements: pd.DataFrame,
                           zscore_threshold: float = 2.5) -> pd.DataFrame:
    '''Returns a dataframe of outliers whose 
    zscores is greater than 2.5 unless specified otherwise.'''
    # threshold will be specified later on based on data observations
    temperature_condition = measurements['temperature_zscore'].abs(
    ) > zscore_threshold
    moisture_condition = measurements['moisture_zscore'].abs(
    ) > zscore_threshold
    return measurements[moisture_condition], measurements[temperature_condition]


def get_outlier_count_per_plant(measurements: pd.DataFrame) -> dict:
    '''Returns the count of outliers in a dictionary where the
      keys are the plant_ids and the values are the outlier counts'''
    moist_outliers, temp_outliers = get_outliers_by_zscore(measurements)
    moist_outlier_count = moist_outliers.groupby(
        ['plant_id'])['plant_id'].count()
    temp_outlier_count = temp_outliers.groupby(
        ['plant_id'])['plant_id'].count()
    return temp_outlier_count, moist_outlier_count


def detect_plant_risks(measurements: pd.DataFrame, threshold: int = 5) -> dict[str:bool]:
    '''Returns the plant id for which sensor is giving 
    more than 'threshold' outliers for moisture or temperature'''
    temp_outlier_count, moist_outlier_count = get_outlier_count_per_plant(
        measurements)
    temp_outlier_count = temp_outlier_count[temp_outlier_count >= threshold]
    moist_outlier_count = moist_outlier_count[moist_outlier_count >= threshold]
    outliers = {'moisture': list(moist_outlier_count.keys()),
                'temperature': list(temp_outlier_count.keys())}
    return outliers


if __name__ == '__main__':
    recent_measurements = get_recent_measurements()
    recent_measurements = add_zscore_columns(recent_measurements)
    print(detect_plant_risks(recent_measurements))
