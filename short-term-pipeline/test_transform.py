import pandas as pd
import pytest
import os
from transform import transform_to_datetime, round_floats, save_clean_data_to_csv


@pytest.fixture
def sample_data():
    """Fixture providing sample plant measurement data as a DataFrame"""
    data = {
        "plant_id": [1, 2],
        "temperature": [25.567, 22.134],
        "moisture": [40.678, 35.456],
        "last_watered": ["2024-03-01", "InvalidDate"],
        "measurement_time": ["2024-03-02 12:30:00", "2024-03-03 15:45:00"]
    }
    return pd.DataFrame(data)


def test_transform_to_datetime(sample_data):
    """Test that date columns are converted to datetime format correctly"""
    transformed = transform_to_datetime(sample_data)

    assert pd.api.types.is_datetime64_any_dtype(
        transformed["measurement_time"])
    assert pd.api.types.is_datetime64_any_dtype(transformed["last_watered"])

    assert pd.isna(transformed["last_watered"][1])


def test_round_floats(sample_data):
    """Test that float values are rounded to 2 decimal places"""
    rounded = round_floats(sample_data)

    assert rounded["temperature"][0] == 25.57
    assert rounded["temperature"][1] == 22.13
    assert rounded["moisture"][0] == 40.68
    assert rounded["moisture"][1] == 35.46


def test_save_clean_data_to_csv(sample_data, tmp_path):
    """Test that clean data is saved correctly to a CSV file"""
    save_clean_data_to_csv(sample_data)

    assert os.path.exists("data/clean-plant-measurements.csv")

    saved_data = pd.read_csv("data/clean-plant-measurements.csv")

    assert saved_data.shape == sample_data.shape

    assert list(saved_data.columns) == list(sample_data.columns)
