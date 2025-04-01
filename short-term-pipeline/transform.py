"""Script to transform plant measurement data to fit the defined schema"""

import pandas as pd


def read_data(file_name: str) -> pd.DataFrame:
    """reading from csv into dataframe"""
    return pd.read_csv(file_name)


def transform_to_datetime(data: pd.DataFrame) -> pd.DataFrame:
    """transforming all columns with a date into datetime objects"""

    data['measurement_time'] = pd.to_datetime(
        data['measurement_time'], errors="coerce")
    data['last_watered'] = pd.to_datetime(
        data['last_watered'], errors="coerce")

    return data


def round_floats(data: pd.DataFrame) -> pd.DataFrame:
    """rounding all temperature and measurement values to 2 d.p"""

    data['temperature'] = data['temperature'].round(2)
    data['moisture'] = data['moisture'].round(2)

    return data


def save_clean_data_to_csv(data: pd.DataFrame):
    """applying all transformations to the dataframe and saving clean
    data to csv file"""

    clean_data = transform_to_datetime(data)
    clean_data = round_floats(data)

    clean_data.to_csv("data/clean-plant-measurements.csv", index=False)


if __name__ == "__main__":

    final_data = read_data("data/plant-measurements.csv")
    save_clean_data_to_csv(final_data)
