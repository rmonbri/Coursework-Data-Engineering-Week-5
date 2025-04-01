'''A script that scrapes the API for seed data'''
import requests
import json
import time


def scrape_endpoints() -> dict:
    seed_data = {"botanist": [], "plant_id": [], "origin": {"latitude": 1}}
    for i in range(0, 60):
        data = make_get_request(
            f"https://data-eng-plants-api.herokuapp.com/plants/{i}")
        botanist = data.get("botanist", "")
        if botanist not in seed_data['botanist']:
            seed_data['botanist'].append(botanist)
        plant_id = data.get('plant_id', "")
        if plant_id not in seed_data['plant_id']:
            seed_data['plant_id'].append(plant_id)
        plant_name = data.get("name", "")
        if plant_name not in seed_data["plant_type"]['plant_name']:
            seed_data["plant_type"]['plant_name'].append(plant_name)
        scientific_name = data.get("scientific_name"[0], "")
        if plant_name not in seed_data["plant_type"]['scientific_name']:
            seed_data["plant_type"]['scientific_name'].append(scientific_name)
        origin = data.get("origin_location", "")
        if origin not in seed_data['origin']:
            seed_data['origin'].append(origin)
        print(seed_data)
    return seed_data


def get_seed_data():
    seed_data = {"botanist": [], "origin": [], "plant_type": []}
    for i in range(0, 60):
        data = make_get_request(
            f"https://data-eng-plants-api.herokuapp.com/plants/{i}")
        seed_data = get_botanist(data, seed_data)
        seed_data = get_origin(data, seed_data)
        seed_data = get_plant_type(data, seed_data)

    return seed_data


def get_botanist(data, seed_data):
    botanist = data.get("botanist", "")
    if botanist and botanist not in seed_data['botanist']:
        seed_data['botanist'].append(botanist)
    return seed_data


def get_origin(data, seed_data):
    origin = data.get("origin_location", "")
    if origin:
        origin_dict = {"latitude": origin[0], "longitude": origin[1],
                       "locality": origin[2], "country_code": origin[3], "timezone": origin[4]}
        if origin_dict not in seed_data['origin']:
            seed_data['origin'].append(origin_dict)
    return seed_data


def get_plant_type(data, seed_data):
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
    return seed_data


def make_get_request(url: str) -> dict:
    res = requests.get(url)
    if res.status_code == 200:
        return json.loads(res.content)
    return {"error": "page not found"}


if __name__ == "__main__":
    start = time.time()
    seed_data = get_seed_data()
    end = time.time()
    print(f"This calculation took {end - start} seconds")
    print(seed_data)
