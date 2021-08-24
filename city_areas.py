from config import base_url, auth_params
from model import CityArea
import country
import worldcities
import csv
import requests
import json


response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}


def get_city_area_by_name(city_area_name):
    headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
    local_response = requests.get(base_url + '/api/_search/city-areas', headers=headers,
                                  data={'query': city_area_name})
    if local_response.status_code != 500:
        local_response = local_response.json()
        if len(local_response) > 0 and local_response[0] is not None \
                and (local_response[0]['name']).lower() == city_area_name.lower():
            city_area = CityArea()
            city_area.id = local_response[0]['id']
            city_area.name = local_response[0]['name']
            city_area.urduName = local_response[0]['urduName']
            city_area.city = local_response[0]['city']            
            return city_area


def import_city_areas():
    with open("./csv/city_areas.csv", encoding='utf-8') as files:
        reader = csv.reader(files)
        next(reader, None)
        for data in reader:
            if get_city_area_by_name(data[0].strip()) is None:
                local_city = worldcities.get_city_by_name(data[1].strip())
                if local_city is not None:
                    local_country = None                    
                    if data[2] is not None:
                        local_country = country.get_country_by_name(data[2].strip())
                        if local_country is not None:
                            city_area = CityArea()
                            city_area.name = data[0].strip()
                            local_city.country = None
                            city_area.city = local_city
                            city_area_json = json.dumps(city_area.__dict__,
                                                    default=city_area.encode_associations)
                            headers.update({'Content-Type': 'application/json'})
                            requests.post(base_url + '/api/city-areas', headers=headers, data=city_area_json)



