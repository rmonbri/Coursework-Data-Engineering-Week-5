"""Script to transform plant measurement data to fit the defined schema"""

import pandas as pd
from datetime import timedelta


def read_csv_data(file_name: str) -> pd.DataFrame:
    """reading from csv into dataframe"""
    return pd.read_csv(file_name)


def read_data(data: list[dict]) -> pd.DataFrame:
    """reading from list of data"""
    return pd.DataFrame(data)


def transform_to_datetime(data: pd.DataFrame) -> pd.DataFrame:
    """transforming all columns with a date into datetime objects"""

    data['measurement_time'] = pd.to_datetime(
        data['measurement_time'], errors="coerce")
    data['last_watered'] = pd.to_datetime(
        data['last_watered'], errors="coerce")

    return data


def correct_timezones(data: pd.DataFrame) -> pd.DataFrame:
    '''Corrects measurement time to account for Daylight saving times'''
    data['measurement_time'] = data['measurement_time'].apply(
        lambda x: x+timedelta(hours=1))
    data['last_watered'] = data['last_watered'].apply(
        lambda x: x+timedelta(hours=1))
    return data


def round_floats(data: pd.DataFrame) -> pd.DataFrame:
    """rounding all temperature and measurement values to 2 d.p"""

    data['temperature'] = data['temperature'].round(2)
    data['moisture'] = data['moisture'].round(2)

    return data


def clean_data(data: pd.DataFrame) -> pd.DataFrame:

    clean_data = transform_to_datetime(data)
    clean_data = round_floats(clean_data)
    clean_data = correct_measurement_time(clean_data)

    return clean_data


def save_clean_data_to_csv(data: pd.DataFrame):
    """applying all transformations to the dataframe and saving clean
    data to csv file"""

    data.to_csv("data/clean-plant-measurements.csv", index=False)
    print("Clean data saved to clean-plant-measurements.csv")


if __name__ == "__main__":

    final_data = read_csv_data("data/plant-measurements.csv")
    cleaned_data = clean_data(final_data)
    save_clean_data_to_csv(cleaned_data)
