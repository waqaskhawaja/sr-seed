from model import Gender
import csv
import requests
import json

base_url = 'http://localhost:8080'

auth_params = {'username':'admin','password':'admin'}
response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}

def get_gender_by_name(gender_name):
    response = requests.get(base_url + '/api/_search/genders', headers=headers, data={'query':gender_name})
    if(response.status_code) != 500:
        response = response.json()
        if len(response) > 0 and response[0] is not None and response[0]['name'] == gender_name:
            gender = Gender()
            gender.id = response[0]['id']
            gender.name = response[0]['name']            
            gender.urduName = response[0]['urduName']            
            return gender


def import_genders():
    with open("./csv/gender.csv", encoding='utf-8') as files:
        reader = csv.reader(files)
        next(reader, None)
        for data in reader:                        
            if get_gender_by_name(data[0].strip()) is None:
                gender = {}
                gender['name'] = data[0].strip()
                gender['urduName'] = data[1].strip()
                local_response = requests.post(base_url + '/api/genders', headers=headers, json=gender)
                print(local_response.request.body)


