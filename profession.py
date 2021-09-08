from config import base_url, auth_params
from model import Profession
import csv
import requests
import json


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}


def get_profession_by_name(profession_name):
    headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
    local_response = requests.get(base_url + '/api/_search/professions', headers=headers,
                                  data={'query': profession_name})
    if local_response.status_code != 500:
        local_response = local_response.json()
        if len(local_response) > 0 and local_response[0] is not None \
                and (local_response[0]['name']).lower() == profession_name.lower():
            profession = Profession()
            profession.id = local_response[0]['id']
            profession.name = local_response[0]['name']
            return profession


def populate_profession(row):
    profession = Profession()
    profession.name = row["preferredLabel"].strip().title()
    profession.conceptUri = row["conceptUri"]
    profession.iscoGroup = row["iscoGroup"]
    profession.description = row["description"]        
    return profession


def import_professions():
    with open("./csv/occupations_en.csv", encoding='utf-8') as files:
        reader = csv.DictReader(files)
        next(reader, None)
        for data in reader:
            try:
                if data["preferredLabel"] is not None and data["preferredLabel"].strip() is not None and get_profession_by_name(data["preferredLabel"].strip()) is None:
                    profession = populate_profession(data)
                    headers.update({'Content-Type': 'application/json'})
                    profession_json = json.dumps(profession.__dict__, default=profession.encode_parent)
                    profession_response = requests.post(base_url + '/api/professions',headers=headers, data=profession_json)
                    if profession_response.status_code == 201:
                        profession_response = profession_response.json()
                        profession.id = profession_response["id"]
                        profession_children = data["altLabels"].splitlines()
                        for child_profession_name in profession_children:
                            child_profession = Profession()
                            child_profession.name = child_profession_name.title()
                            child_profession.parent = profession
                            profession_json = json.dumps(child_profession.__dict__, default=child_profession.encode_parent)
                            headers.update({'Content-Type': 'application/json'})
                            requests.post(base_url + '/api/professions', headers=headers, data=profession_json)
                            
            except IndexError:
                print(data)
