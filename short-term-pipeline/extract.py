"""Script to extract all plant measurements from API and save to csv file"""
import requests
import csv
import multiprocessing
import time

BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"


def get_plant_data(id: int):
    """Function that connects to the API and retrieves a response for a given id"""

    plant_url = f"{BASE_URL}{id}"

    retries = 3

    for attempt in range(retries):
        response = requests.get(plant_url)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 500:
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
        plant_data = pool.map(get_plant_data, range(1, 51))

    return [plant for plant in plant_data if plant]


def save_to_csv(data: list[dict], file_name: str):
    """Function to save the plant measurement data to a csv file"""

    if not data:
        print('Nothing to save')
        return
    columns = ["plant_id", "name", "temperature",
               "soil_moisture", "last_watered"]
    with open(file_name, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()

        for plant in data:
            writer.writerow({
                "plant_id": plant.get("plant_id", ""),
                "name": plant.get("name", ""),
                "temperature": plant.get("temperature", ""),
                "soil_moisture": plant.get("soil_moisture", ""),
                "last_watered": plant.get("last_watered", "")

            })


if __name__ == "__main__":
    start = time.time()
    plant_data = get_plant_data_multiprocessing()
    save_to_csv(plant_data, "plants.csv")
    end = time.time()

    print(f"Time to run: {end-start}")
