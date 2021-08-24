from config import base_url, auth_params
from model import LanguageProficiency
import csv
import requests
import json


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}


def get_language_proficiency_by_name(language_proficiency_name):
    local_response = requests.get(base_url + '/api/_search/language-proficiencies', headers=headers,
                                  data={'query': language_proficiency_name})
    if local_response.status_code != 500:
        local_response = local_response.json()
        if len(local_response) > 0 and local_response[0] is not None \
                and (local_response[0]['name']).lower() == language_proficiency_name.lower():
            language_proficiency = LanguageProficiency()
            language_proficiency.id = local_response[0]['id']
            language_proficiency.name = local_response[0]['name']
            language_proficiency.level = local_response[0]['level']
            return language_proficiency


def import_language_proficiencies():
    with open("./csv/language_proficiencies.csv", encoding='utf-8') as files:
        reader = csv.reader(files)
        next(reader, None)
        for data in reader:                        
            if get_language_proficiency_by_name(data[0].strip()) is None:
                language_proficiency = {'level': data[0].strip(), 'name': data[1].strip()}
                requests.post(base_url + '/api/language-proficiencies', headers=headers, json=language_proficiency)
