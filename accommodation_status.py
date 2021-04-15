from config import base_url, auth_params
from model import AccommodationStatus
import csv
import requests
import json


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}


def get_accommodation_status_by_name(accommodation_status_name):
    local_response = requests.get(base_url + '/api/_search/accommodation-statuses', headers=headers,
                                  data={'query': accommodation_status_name})
    if local_response.status_code != 500:
        local_response = local_response.json()
        if len(local_response) > 0 and local_response[0] is not None \
                and local_response[0]['name'] == accommodation_status_name:
            accommodation_status = AccommodationStatus()
            accommodation_status.id = local_response[0]['id']
            accommodation_status.name = local_response[0]['name']
            return accommodation_status


def import_accommodation_statuses():
    with open("./csv/accommodation_status.csv", encoding='utf-8') as files:
        reader = csv.reader(files)
        next(reader, None)
        for data in reader:                        
            if get_accommodation_status_by_name(data[0].strip()) is None:
                accommodation_status = {'name': data[0].strip()}
                requests.post(base_url + '/api/accommodation-statuses', headers=headers, json=accommodation_status)



