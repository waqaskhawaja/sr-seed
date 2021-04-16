from config import base_url, auth_params
from model import CountryAdminUnit
import country_admin_unit_type
import csv
import requests
import json


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}


def get_country_admin_unit_by_name(country_admin_unit_name):
    headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
    local_response = requests.get(base_url + '/api/_search/country-admin-units', headers=headers,
                                  data={'query': country_admin_unit_name})
    if local_response.status_code != 500:
        local_response = local_response.json()
        if len(local_response) > 0 and local_response[0] is not None \
                and local_response[0]['name'] == country_admin_unit_name:
            country_admin_unit = CountryAdminUnit()
            country_admin_unit.id = local_response[0]['id']
            country_admin_unit.name = local_response[0]['name']
            country_admin_unit.urduName = local_response[0]['urduName']
            country_admin_unit.countryAdminUnitType = local_response[0]['countryAdminUnitType']
            country_admin_unit.parent = local_response[0]['parent']
            return country_admin_unit


def import_country_admin_unit():
    with open("./csv/country_admin_units.csv", encoding='utf-8') as files:
        reader = csv.reader(files)
        next(reader, None)
        for data in reader:
            if get_country_admin_unit_by_name(data[0].strip()) is None:
                parent = None
                local_country_admin_unit_type = None
                if data[2] is not None:
                    local_country_admin_unit_type = \
                        country_admin_unit_type.get_country_admin_unit_type_by_name(data[2].strip())
                if data[3] is not None:
                    parent = get_country_admin_unit_by_name(data[3].strip())
                country_admin_unit = CountryAdminUnit()
                country_admin_unit.name = data[0].strip().title()
                country_admin_unit.urduName = data[1].strip()
                country_admin_unit.parent = parent
                country_admin_unit.countryAdminUnitType = local_country_admin_unit_type
                caste_json = json.dumps(country_admin_unit.__dict__,
                                        default=country_admin_unit.encode_associations)
                headers.update({'Content-Type': 'application/json'})
                requests.post(base_url + '/api/country-admin-units', headers=headers, data=caste_json)



