"""Script to transform plant measurement data to fit the defined schema"""

import csv
import pandas as pd


def read_data(file_name: str) -> pd.DataFrame:

    return pd.read_csv(file_name)


def transform_to_datetime(data: pd.DataFrame) -> pd.DataFrame:

    data['measurement_time'] = pd.to_datetime(
        data['measurement_time'], errors="coerce")
    data['last_watered'] = pd.to_datetime(
        data['last_watered'], errors="coerce")

    return data


def round_floats(data: pd.DataFrame) -> pd.DataFrame:

    data['temperature'] = data['temperature'].round(2)
    data['moisture'] = data['moisture'].round(2)

    return data


def save_clean_data_to_csv(data: pd.DataFrame):

    clean_data = transform_to_datetime(data)
    clean_data = round_floats(data)

    clean_data.to_csv("clean_measurements.csv", index=False)


if __name__ == "__main__":

    data = read_data("plants.csv")
    save_clean_data_to_csv(data)
