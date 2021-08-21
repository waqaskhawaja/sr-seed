from config import base_url, auth_params
from model import EducationalInstitute
import csv
import requests
import json
import educational_institute_type
import country


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}


def get_educational_institute_by_name(educational_institute_name):
    headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
    local_response = requests.get(base_url + '/api/_search/educational-institutes', headers=headers,
                                  data={'query': educational_institute_name})
    if local_response.status_code != 500:
        local_response = local_response.json()
        if len(local_response) > 0 and local_response[0] is not None \
                and local_response[0]['name'] == educational_institute_name:
            educational_institute = EducationalInstitute()
            educational_institute.id = local_response[0]['id']
            educational_institute.name = local_response[0]['name']
            educational_institute.educationalInstituteType = local_response[0]['educationInstituteType']
            educational_institute.country = local_response[0]['country']            
            return educational_institute


def import_educational_institute():
    with open("./csv/world-universities.csv", encoding='utf-8') as files:
        reader = csv.DictReader(files)
        next(reader, None)
        local_educational_institute_type = None                
        local_educational_institute_type = educational_institute_type.get_educational_institute_type_by_name("University")
        for data in reader:
            if data["Name"] is not None and get_educational_institute_by_name(data["Name"].strip()) is None:
                country_obj = None
                if data["CountryCode"] is not None:
                    country_obj = country.get_country_by_iso_code(data["CountryCode"])
                educational_institute = EducationalInstitute()
                educational_institute.name = data["Name"].strip()                
                educational_institute.country = country_obj
                educational_institute.educationInstituteType = local_educational_institute_type
                educational_institute_json = json.dumps(educational_institute.__dict__,
                                        default=educational_institute.encode_associations)
                headers.update({'Content-Type': 'application/json'})
                requests.post(base_url + '/api/educational-institutes', headers=headers, data=educational_institute_json)



