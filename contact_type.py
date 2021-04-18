from config import base_url, auth_params
from model import ContactType
import csv
import requests
import json


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}


def get_contact_type_by_name(contact_type_name):
    local_response = requests.get(base_url + '/api/_search/contact-types', headers=headers,
                                  data={'query': contact_type_name})
    if local_response.status_code != 500:
        local_response = local_response.json()
        if len(local_response) > 0 and local_response[0] is not None \
                and (local_response[0]['name']).lower() == contact_type_name.lower():
            contact_type = ContactType()
            contact_type.id = local_response[0]['id']
            contact_type.name = local_response[0]['name']
            return contact_type


def import_contact_types():
    with open("./csv/contact_type.csv", encoding='utf-8') as files:
        reader = csv.reader(files)
        next(reader, None)
        for data in reader:                        
            if get_contact_type_by_name(data[0].strip()) is None:
                contact_type = {'name': data[0].strip()}
                requests.post(base_url + '/api/contact-types', headers=headers, json=contact_type)
