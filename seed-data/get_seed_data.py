# pylint: disable=duplicate-code
'''A script that scrapes the API for seed data'''
import csv
import json
import time
import requests


BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"
NUM_PLANTS = 51


def make_get_request(plant_id: int) -> dict:
    '''Makes a get request, attempting thrice before failing'''
    url = f"{BASE_URL}{plant_id}"

    retries = 3

    for attempt in range(retries):
        response = requests.get(url, timeout=30)

        if response.status_code == 200:
            return json.loads(response.content)
        if response.status_code == 500:
            print(
                f"Status code 500 for plant ID {plant_id}, retrying... (Attempt {attempt + 1})")
            time.sleep(2)
        else:
            print(
                f"Failed to fetch data for plant ID {plant_id}: {response.status_code}")
            return None

    print(f"Giving up on plant ID {plant_id} after {retries} attempts.")
    return None


def get_seed_data() -> dict:
    '''Sorts API get request information into a seed_data dictionary'''
    seed_data = {"botanist": [], "origin": [],
                 "plant_type": [], "plant_id": []}
    for plant_id in range(0, NUM_PLANTS):
        data = make_get_request(plant_id)
        if data:
            (seed_data, botanist_data) = get_botanist(data, seed_data)
            (seed_data, origin_data) = get_origin(data, seed_data)
            (seed_data, plant_type_data) = get_plant_type(data, seed_data)

            seed_data = get_plant_id(
                data, seed_data, botanist_data, origin_data, plant_type_data)

    return seed_data


def get_plant_id(data, seed_data, botanist_data, origin_data, plant_type_data):
    '''Returns the values for plant_id to the seed_data dictionary'''
    plant_id = data.get("plant_id", "")
    botanist_id = seed_data['botanist'].index(botanist_data)
    origin_id = seed_data['origin'].index(origin_data)
    plant_type_id = seed_data['plant_type'].index(plant_type_data)

    plant_id_dict = {'plant_id': plant_id,
                     'botanist_id': botanist_id + 1,
                     'origin_data': origin_id + 1,
                     'plant_type_id': plant_type_id + 1}

    if plant_id is not None and plant_id not in seed_data['plant_id']:
        seed_data['plant_id'].append(plant_id_dict)
    return seed_data


def get_botanist(data, seed_data):
    '''Returns the values for botanist to the seed_data dictionary'''
    botanist = data.get("botanist", "")
    if botanist and botanist not in seed_data['botanist']:
        seed_data['botanist'].append(botanist)
    return seed_data, botanist


def get_origin(data, seed_data):
    '''Returns the values for origin to the seed_data dictionary'''
    origin = data.get("origin_location", "")
    if origin:
        origin_dict = {"latitude": origin[0], "longitude": origin[1],
                       "locality": origin[2], "country_code": origin[3], "timezone": origin[4]}
        if origin_dict not in seed_data['origin']:
            seed_data['origin'].append(origin_dict)
    return seed_data, origin_dict


def get_plant_type(data, seed_data):
    '''Returns the values for plant_type to the seed_data dictionary'''
    plant_name = data.get("name", "")
    if plant_name:
        plant_name_dict = {}
        scientific_name = data.get("scientific_name", "None")
        if scientific_name != "None":
            scientific_name = scientific_name[0]
        plant_name_dict['plant_name'] = plant_name
        plant_name_dict["scientific_name"] = scientific_name
        if plant_name_dict not in seed_data['plant_type']:
            seed_data['plant_type'].append(plant_name_dict)
    return seed_data, plant_name_dict


def save_all_data_to_csv(seed_data):
    '''Saves seed data as a CSV file, ready to be seeded'''
    if not seed_data:
        print("No seed data available.")
        return

    save_botanist_data_as_csv(seed_data)
    save_origin_data_as_csv(seed_data)
    save_plant_type_data_as_csv(seed_data)
    save_plant_id_data_as_csv(seed_data)


def save_botanist_data_as_csv(seed_data):
    '''Saves botanist data to csv'''
    print("Saving botanist data to csv...")
    with open('botanist.csv', 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames = ['name', 'email', 'phone']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for values in seed_data['botanist']:
            writer.writerow(values)
    print("botanist.csv created!")


def save_plant_id_data_as_csv(seed_data):
    '''Saves plant_id data to csv'''
    print("Saving plant_id data to csv...")
    with open('plant_id.csv', 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames = ['plant_id', 'botanist_id',
                      'origin_data', 'plant_type_id',]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for values in seed_data['plant_id']:
            writer.writerow(values)
    print("plant_id.csv created!")


def save_origin_data_as_csv(seed_data):
    '''Saves origin data to csv'''
    print("Saving origin data to csv...")
    with open('origin.csv', 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames = ["latitude", "longitude",
                      "locality", "country_code", "timezone"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for values in seed_data['origin']:
            writer.writerow(values)
    print("origin.csv created!")


def save_plant_type_data_as_csv(seed_data):
    '''Saves plant type data to csv'''
    print("Saving plant_type data to csv...")
    with open('plant_type.csv', 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames = ["plant_name", "scientific_name"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for values in seed_data['plant_type']:
            writer.writerow(values)
    print("plant_type.csv created!")


if __name__ == "__main__":
    start = time.time()
    complete_seed_data = get_seed_data()
    end = time.time()
    print(f"This calculation took {end - start} seconds")
    save_all_data_to_csv(complete_seed_data)
