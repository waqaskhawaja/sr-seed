from config import base_url, auth_params
from model import Sect
import religion
import csv
import requests
import json


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}


def get_sect_by_name(sect_name):
    headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
    local_response = requests.get(base_url + '/api/_search/sects', headers=headers,
                                  data={'query': sect_name})
    if local_response.status_code != 500:
        local_response = local_response.json()
        if len(local_response) > 0 and local_response[0] is not None \
                and local_response[0]['name'] == sect_name:
            sect = Sect()
            sect.id = local_response[0]['id']
            sect.name = local_response[0]['name']
            sect.urduName = local_response[0]['urduName']
            sect.religion = local_response[0]['religion']
            sect.parent = local_response[0]['parent']
            return sect


def import_sect():
    with open("./csv/sect.csv", encoding='utf-8') as files:
        reader = csv.reader(files)
        next(reader, None)
        for data in reader:
            if get_sect_by_name(data[0].strip()) is None:
                parent = None
                local_religion = None
                if data[2] is not None:
                    local_religion = religion.get_religion_by_name(data[2].strip())
                if data[3] is not None:
                    parent = get_sect_by_name(data[3].strip())
                sect = Sect()
                sect.name = data[0].strip().title()
                sect.urduName = data[1].strip()
                sect.parent = parent
                sect.religion = local_religion
                caste_json = json.dumps(sect.__dict__,
                                        default=sect.encode_associations)
                headers.update({'Content-Type': 'application/json'})
                requests.post(base_url + '/api/sects', headers=headers, data=caste_json)



