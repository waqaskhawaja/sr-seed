from config import base_url, auth_params
from model import Language
import csv
import requests
import json


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}


def get_language_by_name(language_name):
    headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
    local_response = requests.get(base_url + '/api/_search/languages', headers=headers,
                                  data={'query': language_name})
    if local_response.status_code != 500:
        local_response = local_response.json()
        if len(local_response) > 0 and local_response[0] is not None \
                and (local_response[0]['name']).lower() == language_name.lower():
            language = Language()
            language.id = local_response[0]['id']
            language.name = local_response[0]['name']
            language.nativeName = local_response[0]['nativeName']
            language.code6391 = local_response[0]['code6391']
            language.code6392B = local_response[0]['code6392B']
            language.code6392T = local_response[0]['code6392T']
            return language


def import_languages():
    with open("./csv/languages_list.csv", encoding='utf-8') as files:
        reader = csv.DictReader(files)
        next(reader, None)
        for data in reader:                        
            if get_language_by_name(data["Language name"].strip()) is None:                
                language_2 = {"name": data['Language name'].strip(), "nativeName": data['Native name'].strip(), "code6391": data['6391'].strip(), "code6392T": data['6392T'].strip(), "code6392B": data['6392B'].strip()}                                
                headers.update({'Content-Type': 'application/json'})
                requests.post(base_url + '/api/languages', headers=headers, json=language_2)
