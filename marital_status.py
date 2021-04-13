from config import base_url, auth_params
from model import MaritalStatus
import csv
import requests
import json


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}

def get_marital_status_by_name(marital_status_name):
    response = requests.get(base_url + '/api/_search/marital-statuses', headers=headers, data={'query':marital_status_name})
    if(response.status_code) != 500:
        response = response.json()
        if len(response) > 0 and response[0] is not None and response[0]['name'] == marital_status_name:
            marital_status = MaritalStatus()
            marital_status.id = response[0]['id']
            marital_status.name = response[0]['name']            
            marital_status.urduName = response[0]['urduName']            
            return marital_status


def import_marital_statuses():
    with open("./csv/marital_status.csv", encoding='utf-8') as files:
        reader = csv.reader(files)
        next(reader, None)
        for data in reader:                        
            if get_marital_status_by_name(data[0].strip()) is None:
                marital_status = {'name': data[0].strip(), 'urduName': data[1].strip()}
                requests.post(base_url + '/api/marital-statuses',headers=headers, json=marital_status)
