"""Tests for the load script"""

from unittest.mock import mock_open
import pytest
from unittest.mock import patch, MagicMock
from load import (get_connection_to_db, get_measurements, upload_many_rows,
                  ingress_measurements_to_db)


@pytest.fixture
def fake_data():
    """Fixture providing sample data"""
    return [
        (1, 25.5, 40, "2024-03-01", "2024-03-02 12:30:00"),
        (2, 22.0, 35, "2024-03-02", "2024-03-03 15:45:00")
    ]


@patch("load.pymssql.connect")
def test_get_connection_to_db(mock_connect):
    """Test that database connection is established"""
    mock_connect.return_value = MagicMock()

    conn = get_connection_to_db()

    mock_connect.assert_called_once()
    assert conn is not None


@patch("builtins.open", new_callable=mock_open,
       read_data="plant_id,temperature,moisture,last_watered,measurement_time\n1,25.5,40,2024-03-01,2024-03-02 12:30:00\n2,22.0,35,2024-03-02,2024-03-03 15:45:00\n")
def test_get_measurements(mock_file):
    """Test that measurements are correctly read from CSV"""
    measurements = get_measurements()

    assert len(measurements) == 2
    assert measurements[0] == (
        "1", "25.5", "40", "2024-03-01", "2024-03-02 12:30:00")


@patch("load.pymssql.Connection")
def test_upload_many_rows(mock_conn, fake_data):
    """Test that multiple rows are inserted into the database"""
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    upload_many_rows(fake_data, mock_conn)

    mock_cursor.executemany.assert_called_once()

    executed_sql = mock_cursor.executemany.call_args[0][0].strip()
    assert executed_sql.startswith("INSERT into measurement")


@patch("load.get_connection_to_db")
@patch("load.upload_many_rows")
def test_ingress_measurements_to_db(mock_upload, mock_get_conn, fake_data):
    """Test that measurements are uploaded to the database"""
    mock_conn = MagicMock()
    mock_get_conn.return_value = mock_conn

    ingress_measurements_to_db(fake_data)

    mock_upload.assert_called_once_with(fake_data, mock_conn)
    mock_conn.close.assert_called_once()
