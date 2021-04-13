from config import base_url, auth_params
from model import Gender
import csv
import requests
import json


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}


def get_gender_by_name(gender_name):
    local_response = requests.get(base_url + '/api/_search/genders', headers=headers, data={'query': gender_name})
    if local_response.status_code != 500:
        local_response = local_response.json()
        if len(local_response) > 0 and local_response[0] is not None and local_response[0]['name'] == gender_name:
            gender = Gender()
            gender.id = local_response[0]['id']
            gender.name = local_response[0]['name']
            gender.urduName = local_response[0]['urduName']
            return gender


def import_genders():
    with open("./csv/gender.csv", encoding='utf-8') as files:
        reader = csv.reader(files)
        next(reader, None)
        for data in reader:                        
            if get_gender_by_name(data[0].strip()) is None:
                gender = {'name': data[0].strip(), 'urduName': data[1].strip()}
                requests.post(base_url + '/api/genders', headers=headers, json=gender)



