from config import base_url, auth_params
from model import PersonRelationshipType
import csv
import requests
import json


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}


def get_person_relationship_type_by_name(person_relationship_type_name):
    if person_relationship_type_name is not None and person_relationship_type_name != '':
        local_response = requests.get(base_url + '/api/_search/person-relationship-types', headers=headers,
                                      data={'query': person_relationship_type_name})
        if local_response.status_code != 500:
            local_response = local_response.json()
            if len(local_response) > 0 and local_response[0] is not None \
                    and (local_response[0]['name']).lower() == person_relationship_type_name.lower():
                person_relationship_type = PersonRelationshipType
                person_relationship_type.id = local_response[0]['id']
                person_relationship_type.name = local_response[0]['name']
                person_relationship_type.urduName = local_response[0]['urduName']
                return person_relationship_type


def import_person_relationship_type():
    with open("./csv/person_relationship_type.csv", encoding='utf-8') as files:
        reader = csv.reader(files)
        next(reader, None)
        for data in reader:                        
            if get_person_relationship_type_by_name(data[0].strip()) is None:
                person_relationship_type = {'name': data[0].strip().title(), 'urduName': data[1].strip().title()}
                requests.post(base_url + '/api/person-relationship-types', headers=headers, json=person_relationship_type)



