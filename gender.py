from model import Gender
import csv
import requests
import json

base_url = 'http://localhost:9000'

auth_params = {'username':'admin','password':'admin'}
response = requests.post(base_url + '/api/authenticate', json=auth_params)
id_token = (json.loads(response.text))['id_token']
headers = {"Authorization": "Bearer " + id_token}

def get_gender_by_name(gender):
    response = requests.get(base_url + '/api/_search/genders', headers=headers, data={'query':gender})
    if(response.status_code) != 500:
        response = response.json()
        if len(response) > 0 and response[0] is not None and response[0]['name'] == gender:
            gender = Gender()
            gender.id = response[0]['id']
            gender.name = response[0]['name']            
            gender.urdu_name = response[0]['urduName']            
            return gender


def import_genders():
    with open("./csv/gender.csv", encoding='utf-8') as files:
        reader = csv.reader(files)
        next(reader, None)
        for data in reader:                        
            if get_gender_by_name(data[0]) is None:
                gender = {}
                gender['name'] = data[0]                
                gender['urduName'] = data[1]                
                response = requests.post(base_url + '/api/genders',headers=headers, json=gender)


