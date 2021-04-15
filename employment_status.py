from config import base_url, auth_params
from model import EmploymentStatus
import csv
import requests
import json


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}


def get_employment_status_by_name(employment_status_name):
    local_response = requests.get(base_url + '/api/_search/employment-statuses', headers=headers,
                                  data={'query': employment_status_name})
    if local_response.status_code != 500:
        local_response = local_response.json()
        if len(local_response) > 0 and local_response[0] is not None \
                and local_response[0]['name'] == employment_status_name:
            employment_status = EmploymentStatus()
            employment_status.id = local_response[0]['id']
            employment_status.name = local_response[0]['name']
            return employment_status


def import_employment_statuses():
    with open("./csv/employment_status.csv", encoding='utf-8') as files:
        reader = csv.reader(files)
        next(reader, None)
        for data in reader:                        
            if get_employment_status_by_name(data[0].strip()) is None:
                employment_status = {'name': data[0].strip()}
                requests.post(base_url + '/api/employment-statuses', headers=headers, json=employment_status)



