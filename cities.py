from config import base_url, auth_params
from model import City
import country
import country_admin_unit
import csv
import requests
import json
import residence_measurement_unit


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}


def get_city_by_name(city_name):
    headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
    local_response = requests.get(base_url + '/api/_search/cities', headers=headers,
                                  data={'query': city_name})
    if local_response.status_code != 500:
        local_response = local_response.json()
        if len(local_response) > 0 and local_response[0] is not None \
                and (local_response[0]['name']).lower() == city_name.lower():
            city = City()
            city.id = local_response[0]['id']
            city.name = local_response[0]['name']
            city.urduName = local_response[0]['urduName']
            city.latitude = local_response[0]['latitude']
            city.longitude = local_response[0]['longitude']
            city.latitude = local_response[0]['latitude']
            city.population = local_response[0]['population']
            city.capital = local_response[0]['capital']
            city.residenceMeasurementUnit = local_response[0]['residenceMeasurementUnit']
            city.country = local_response[0]['country']
            city.adminUnit = local_response[0]['adminUnit']
            return city


def import_city():
    with open("./csv/worldcities.csv", encoding='utf-8') as files:
        reader = csv.reader(files)
        next(reader, None)
        for data in reader:
            if get_city_by_name(data[0].strip()) is None:
                local_country = None
                admin_unit = None
                local_residence_measurement_unit = None
                if data[4] is not None:
                    local_country = country.get_country_by_name(data[4].strip())
                if data[7] is not None:
                    admin_unit = country_admin_unit.get_country_admin_unit_by_name(data[7].strip())
                if data[10] is not None:
                    local_residence_measurement_unit = residence_measurement_unit.get_residence_measurement_unit_by_name(data[10])
                city = City()
                city.name = data[0].strip().title()
                city.latitude = data[2].strip()
                city.longitude = data[3].strip()
                city.capital = True if data[8] == 'primary' else False
                city.population = data[9].strip()
                city.country = local_country
                city.adminUnit = admin_unit
                city.residenceMeasurementUnit = local_residence_measurement_unit
                caste_json = json.dumps(city.__dict__,
                                        default=city.encode_associations)
                headers.update({'Content-Type': 'application/json'})
                requests.post(base_url + '/api/cities', headers=headers, data=caste_json)



