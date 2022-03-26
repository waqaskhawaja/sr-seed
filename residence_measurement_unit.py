from config import base_url, auth_params
from model import ResidenceMeasurementUnit
import csv
import requests
import json


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}


def get_residence_measurement_unit_by_name(residence_measurement_unit_name):
    local_response = requests.get(base_url + '/api/_search/resident-measurement-units', headers=headers,
                                  data={'query': residence_measurement_unit_name})
    if local_response.status_code != 500 and local_response.status_code != 404:
        local_response = local_response.json()
        if len(local_response) > 0 and local_response[0] is not None \
                and local_response[0]['name'] == residence_measurement_unit_name:
            residence_measurement_unit = ResidenceMeasurementUnit()
            residence_measurement_unit.id = local_response[0]['id']
            residence_measurement_unit.name = local_response[0]['name']
            return residence_measurement_unit


def import_residence_measurement_unit():
    with open("./csv/residence_measurement_unit.csv", encoding='utf-8') as files:
        reader = csv.reader(files)
        next(reader, None)
        for data in reader:                        
            if get_residence_measurement_unit_by_name(data[0].strip()) is None:
                residence_measurement_unit = {'name': data[0].strip()}
                requests.post(base_url + '/api/residence-measurement-units', headers=headers, json=residence_measurement_unit)



