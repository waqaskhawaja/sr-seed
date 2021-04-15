from config import base_url, auth_params
from model import Religion
import csv
import requests
import json


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}


def get_religion_by_name(religion_name):
    local_response = requests.get(base_url + '/api/_search/religions', headers=headers,
                                  data={'query': religion_name})
    if local_response.status_code != 500:
        local_response = local_response.json()
        if len(local_response) > 0 and local_response[0] is not None \
                and local_response[0]['name'] == religion_name:
            religion = Religion()
            religion.id = local_response[0]['id']
            religion.name = local_response[0]['name']
            return religion


def import_religions():
    with open("./csv/religion.csv", encoding='utf-8') as files:
        reader = csv.reader(files)
        next(reader, None)
        for data in reader:                        
            if get_religion_by_name(data[0].strip()) is None:
                religion = {'name': data[0].strip()}
                requests.post(base_url + '/api/religions', headers=headers, json=religion)
