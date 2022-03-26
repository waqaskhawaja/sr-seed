from config import base_url, auth_params
from model import Ethnicity
import csv
import requests
import json


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}


def get_ethnicity_by_name(ethnicity_name):
    local_response = requests.get(base_url + '/api/_search/ethnicities', headers=headers, data={'query': ethnicity_name})
    if local_response.status_code != 500:
        local_response = local_response.json()
        if len(local_response) > 0 and local_response[0] is not None and local_response[0]['name'] == ethnicity_name:
            ethnicity = Ethnicity()
            ethnicity.id = local_response[0]['id']
            ethnicity.name = local_response[0]['name']
            ethnicity.urduName = local_response[0]['urduName']            
            return ethnicity


def import_ethnicities():
    with open("./csv/ethnicity.csv", encoding='utf-8') as files:
        reader = csv.DictReader(files)
        next(reader, None)
        for data in reader:                        
            if get_ethnicity_by_name(data["Ethnicity"].strip()) is None:
                ethnicity = {'name': data["Ethnicity"].strip()}
                requests.post(base_url + '/api/ethnicities', headers=headers, json=ethnicity)



