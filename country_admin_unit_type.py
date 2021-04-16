from config import base_url, auth_params
from model import CountryAdminUnitType
import country
import csv
import requests
import json


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}


def get_country_admin_unit_type_by_name(country_admin_unit_type_name):
    headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
    local_response = requests.get(base_url + '/api/_search/country-admin-unit-types', headers=headers,
                                  data={'query': country_admin_unit_type_name})
    if local_response.status_code != 500:
        local_response = local_response.json()
        if len(local_response) > 0 and local_response[0] is not None \
                and local_response[0]['name'] == country_admin_unit_type_name:
            country_admin_unit_type = CountryAdminUnitType()
            country_admin_unit_type.id = local_response[0]['id']
            country_admin_unit_type.name = local_response[0]['name']
            country_admin_unit_type.urduName = local_response[0]['urduName']
            country_admin_unit_type.parent = local_response[0]['parent']
            country_admin_unit_type.country = local_response[0]['country']
            return country_admin_unit_type


def import_country_admin_unit_types():
    with open("./csv/country_admin_unit_types.csv", encoding='utf-8') as files:
        reader = csv.reader(files)
        next(reader, None)
        for data in reader:
            if get_country_admin_unit_type_by_name(data[0].strip()) is None:
                parent = None
                local_country = None
                if data[2] is not None:
                    parent = get_country_admin_unit_type_by_name(data[2].strip())
                if data[3] is not None:
                    local_country = country.get_country_by_name(data[3].strip())
                country_admin_unit_type = CountryAdminUnitType()
                country_admin_unit_type.name = data[0].strip().title()
                country_admin_unit_type.urduName = data[1].strip()
                country_admin_unit_type.parent = parent
                country_admin_unit_type.country = local_country
                caste_json = json.dumps(country_admin_unit_type.__dict__,
                                        default=country_admin_unit_type.encode_associations)
                headers.update({'Content-Type': 'application/json'})
                requests.post(base_url + '/api/country-admin-unit-types', headers=headers, data=caste_json)



