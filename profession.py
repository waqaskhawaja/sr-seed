from config import base_url, auth_params
from model import Profession
import csv
import requests
import json


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}


def get_profession_by_name(profession_name):
    local_response = requests.get(base_url + '/api/_search/professions', headers=headers,
                                  data={'query': profession_name})
    if local_response.status_code != 500:
        local_response = local_response.json()
        if len(local_response) > 0 and local_response[0] is not None \
                and local_response[0]['name'] == profession_name:
            profession = Profession()
            profession.id = local_response[0]['id']
            profession.name = local_response[0]['name']
            return profession


def import_professions():
    with open("./csv/professions.csv", encoding='utf-8') as files:
        reader = csv.reader(files)
        next(reader, None)
        for data in reader:                        
            if get_profession_by_name(data[0].strip()) is None:
                profession = {'name': data[0].strip().title()}
                requests.post(base_url + '/api/professions', headers=headers, json=profession)



