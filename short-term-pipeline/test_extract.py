"""Tests for the extract script"""

import csv
from unittest.mock import patch, MagicMock
import pytest
from extract import get_plant_data, save_to_csv


@patch("extract.requests.get")
def test_get_plant_data_success(mock_get):
    """Test successful API response"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"plant_id": 1, "temperature": 25.5}
    mock_get.return_value = mock_response

    result = get_plant_data(1)
    assert result == {"plant_id": 1, "temperature": 25.5}
    mock_get.assert_called_with(
        "https://data-eng-plants-api.herokuapp.com/plants/1", timeout=30)


@patch("extract.requests.get")
def test_get_plant_data_500_retry(mock_get):
    """Test retries when the API returns a 500 error"""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.side_effect = [mock_response, mock_response, mock_response]

    result = get_plant_data(1)
    assert result is None


@patch("extract.requests.get")
def test_get_plant_data_failure(mock_get):
    """Test failure when the API returns a non-500 error"""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    result = get_plant_data(1)
    assert result is None


@pytest.fixture
def sample_data():
    """Fixture providing sample plant measurement data"""
    return [
        {"plant_id": 1, "temperature": 25.5, "soil_moisture": 40,
            "last_watered": "2024-03-01", "recording_taken": "2024-03-02"},
        {"plant_id": 2, "temperature": 22.0, "soil_moisture": 35,
            "last_watered": "2024-03-02", "recording_taken": "2024-03-03"}
    ]


def test_save_to_csv(sample_data, tmp_path):
    """Test saving plant data to CSV file with the correct folder structure"""

    fake_folder = tmp_path / "data"
    fake_folder.mkdir()
    fake_file = fake_folder / "fake_data.csv"

    save_to_csv(sample_data, str(fake_file))

    assert fake_file.exists()

    with open(fake_file, newline='', encoding='utf-8') as f:
        reader = list(csv.reader(f))

    assert reader[0] == ["plant_id", "temperature", "moisture",
                         "last_watered", "measurement_time"]
    assert reader[1] == ["1", "25.5", "40",
                         "2024-03-01", "2024-03-02"]
    assert reader[2] == ["2", "22.0", "35",
                         "2024-03-02", "2024-03-03"]


def test_save_to_csv_empty(tmp_path):
    """Test save_to_csv if there is no data to be saved"""

    fake_folder = tmp_path / "data"
    fake_folder.mkdir()
    fake_file = fake_folder / "fake_data.csv"

    save_to_csv([], str(fake_file))

    assert not fake_file.exists()
