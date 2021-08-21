from config import base_url, auth_params
from model import EducationalInstituteType
import csv
import requests
import json


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}


def get_educational_institute_type_by_name(educational_institute_type_name):
    local_response = requests.get(base_url + '/api/_search/educational-institute-types', headers=headers,
                                  data={'query': educational_institute_type_name})
    if local_response.status_code != 500:
        local_response = local_response.json()
        if len(local_response) > 0 and local_response[0] is not None \
                and (local_response[0]['name']).lower() == educational_institute_type_name.lower():
            educational_institute_type = EducationalInstituteType()
            educational_institute_type.id = local_response[0]['id']
            educational_institute_type.name = local_response[0]['name']
            return educational_institute_type


def import_educational_institute_types():
    with open("./csv/educational_institute_types.csv", encoding='utf-8') as files:
        reader = csv.reader(files)
        next(reader, None)
        for data in reader:                        
            if get_educational_institute_type_by_name(data[0].strip()) is None:
                educational_institute_type = {'name': data[0].strip()}
                requests.post(base_url + '/api/educational-institute-types', headers=headers, json=educational_institute_type)
