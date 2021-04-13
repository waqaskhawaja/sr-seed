from config import base_url, auth_params
from model import EducationLevel
import csv
import requests
import json


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}


def get_education_level_by_name(education_level_name):
    local_response = requests.get(base_url + '/api/_search/education-levels', headers=headers,
                                  data={'query': education_level_name})
    if local_response.status_code != 500:
        local_response = local_response.json()
        if len(local_response) > 0 and local_response[0] is not None \
                and local_response[0]['name'] == education_level_name:
            education_level = EducationLevel()
            education_level.id = local_response[0]['id']
            education_level.name = local_response[0]['name']
            return education_level


def import_education_levels():
    with open("./csv/education_levels.csv", encoding='utf-8') as files:
        reader = csv.reader(files)
        next(reader, None)
        for data in reader:                        
            if get_education_level_by_name(data[0].strip()) is None:
                education_level = {'name': data[0].strip()}
                requests.post(base_url + '/api/education-levels', headers=headers, json=education_level)



