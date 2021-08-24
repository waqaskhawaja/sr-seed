from config import base_url, auth_params
from model import CandidateStatusType
import csv
import requests
import json


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}


def get_candidate_status_type_by_name(candidate_status_type_name):
    local_response = requests.get(base_url + '/api/_search/candidate-status-types', headers=headers,
                                  data={'query': candidate_status_type_name})
    if local_response.status_code != 500:
        local_response = local_response.json()
        if len(local_response) > 0 and local_response[0] is not None \
                and (local_response[0]['name']).lower() == candidate_status_type_name.lower():
            candidate_status_type = CandidateStatusType()
            candidate_status_type.id = local_response[0]['id']
            candidate_status_type.name = local_response[0]['name']
            return candidate_status_type


def import_candidate_status_types():
    with open("./csv/candidate_status_types.csv", encoding='utf-8') as files:
        reader = csv.reader(files)
        next(reader, None)
        for data in reader:                        
            if get_candidate_status_type_by_name(data[0].strip()) is None:
                candidate_status_type = {'name': data[0].strip()}
                requests.post(base_url + '/api/candidate-status-types', headers=headers, json=candidate_status_type)
