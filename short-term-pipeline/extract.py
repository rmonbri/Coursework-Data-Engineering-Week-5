"""Script to extract all plant measurements from API and save to csv file"""

import multiprocessing
import time
import csv
import os
import requests


BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"


def get_plant_data(id: int):
    """Function that connects to the API and retrieves a response for a given id"""

    plant_url = f"{BASE_URL}{id}"

    retries = 3

    for attempt in range(retries):
        response = requests.get(plant_url, timeout=30)

        if response.status_code == 200:
            return response.json()
        if response.status_code == 500:
            print(
                f"Status code 500 for plant ID {id}, retrying... (Attempt {attempt + 1})")
            time.sleep(2)
        else:
            print(
                f"Failed to fetch data for plant ID {id}: {response.status_code}")
            return None

    print(f"Giving up on plant ID {id} after {retries} attempts.")
    return None


def get_plant_data_multiprocessing():
    """Function to get all the plant measurements using multiprocessing"""

    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        plant_data = pool.map(get_plant_data, range(51))

    return [plant for plant in plant_data if plant]


def save_to_csv(data: list[dict], file_name: str):
    """Function to save the plant measurement data to a csv file"""

    if not data:
        print('Nothing to save')
        return
    columns = ["plant_id", "temperature",
               "moisture", "last_watered", "measurement_time"]
    os.makedirs("data", exist_ok=True)
    with open(file_name, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()

        for plant in data:
            writer.writerow({
                "plant_id": plant.get("plant_id", ""),
                "temperature": plant.get("temperature", ""),
                "moisture": plant.get("soil_moisture", ""),
                "last_watered": plant.get("last_watered", ""),
                "measurement_time": plant.get("recording_taken", "")

            })


if __name__ == "__main__":
    start = time.time()
    all_plant_data = get_plant_data_multiprocessing()
    save_to_csv(all_plant_data, "data/plant-measurements.csv")
    end = time.time()

    print(f"Time to run: {end-start}")
