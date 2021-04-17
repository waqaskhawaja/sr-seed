from config import base_url, auth_params
from model import Caste
import csv
import requests
import json


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}


def get_caste_by_name(caste_name):
    headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
    local_response = requests.get(base_url + '/api/_search/castes', headers=headers, data={'query': caste_name})
    if local_response.status_code != 500:
        local_response = local_response.json()
        if len(local_response) > 0 and local_response[0] is not None \
                and (local_response[0]['name']).lower() == caste_name.lower():
            caste = Caste()
            caste.id = local_response[0]['id']
            caste.name = local_response[0]['name']
            caste.urduName = local_response[0]['urduName']
            caste.parent = local_response[0]['parent']
            return caste


def import_castes():
    with open("./csv/castes.csv", encoding='utf-8') as files:
        reader = csv.reader(files)
        next(reader, None)
        for data in reader:                        
            if get_caste_by_name(data[0].strip()) is None:
                parent = None
                if data[2] is not None:
                    parent = get_caste_by_name(data[2].strip())
                caste = Caste()
                caste.name = data[0].strip().title()
                caste.urduName = data[1].strip()
                caste.parent = parent
                caste_json = json.dumps(caste.__dict__, default=caste.encode_parent)
                headers.update({'Content-Type': 'application/json'})
                requests.post(base_url + '/api/castes', headers=headers, data=caste_json)



